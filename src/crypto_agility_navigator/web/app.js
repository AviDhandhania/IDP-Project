/**
 * Crypto-Agility Navigator — Web Dashboard Logic
 * Integrates Python static analysis backend with interactive UI
 */

const PRESETS = {
  archive: `import boto3
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def archive_settlement_record(record_bytes, rsa_public_key):
    # S3 bucket has 10-year regulatory retention policy
    s3 = boto3.client('s3')
    
    ciphertext = rsa_public_key.encrypt(
        record_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    s3.put_object(
        Bucket='bank-settlement-archive-cold-storage',
        Key='records/2026/settlement_audit.enc',
        Body=ciphertext
    )
`,
  session: `import redis
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def store_ephemeral_session(token_data, rsa_public_key):
    # Redis cache with 15-minute TTL
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    enc_token = rsa_public_key.encrypt(
        token_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    r.setex('session:usr_998', 900, enc_token)
`,
  etag: `import hashlib

def calculate_http_etag(resource_body: bytes) -> str:
    # Non-security HTTP cache validator digest
    hasher = hashlib.sha256()
    hasher.update(resource_body)
    return f'W/"{hasher.hexdigest()[:16]}"'
`
};

let currentScanData = null;
let currentFilter = 'all';

// ==========================================
// Initialization
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTabs();
  initSearchAndFilters();
  initMoscaSimulator();
  initCodeScanner();
  initCBOMActions();
  fetchScanData();

  document.getElementById('btn-refresh').addEventListener('click', () => {
    fetchScanData();
  });
});

// ==========================================
// Theme Management
// ==========================================

function initTheme() {
  const toggleBtn = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem('copilot-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  toggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('copilot-theme', next);
  });
}

// ==========================================
// Tabs Management
// ==========================================

function initTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      const targetPane = document.getElementById(tab.getAttribute('data-tab'));
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

// ==========================================
// Data Fetching & Rendering
// ==========================================

async function fetchScanData(target = 'examples/sample_project') {
  try {
    const response = await fetch(`/api/scan?target=${encodeURIComponent(target)}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    currentScanData = data;
    renderAll(data);
  } catch (err) {
    console.warn('API error, using fallback offline mock data:', err);
    // Render fallback data if backend offline
    renderFallbackData();
  }
}

function renderAll(data) {
  renderMetrics(data.metrics, data.targetName);
  renderInventoryTable(data.findings);
  renderDataflowDiagrams(data.findings);
  renderCBOM(data.cbom);
  updateFilterCounts(data.findings);
}

function renderMetrics(m, targetName) {
  document.getElementById('metric-total-findings').textContent = m.totalFindings;
  document.getElementById('metric-shor-broken').textContent = m.shorBrokenCount;
  document.getElementById('metric-mosca-breaches').textContent = m.moscaBreaches;
  document.getElementById('metric-noise-filtered').textContent = `${m.noiseFilteredPercent}%`;
  document.getElementById('metric-noise-detail').textContent = `${m.suppressedCount} noise finding(s) filtered`;
  document.getElementById('metric-avg-score').textContent = m.averageActionableScore;
  if (targetName) {
    document.getElementById('metric-target-name').textContent = `Target: ${targetName}`;
  }
}

function updateFilterCounts(findings) {
  const allCount = findings.length;
  const moscaCount = findings.filter(f => f.moscaViolated).length;
  const actionableCount = findings.filter(f => f.isSecurityRelevant).length;
  const suppressedCount = findings.filter(f => f.urgencyTier === 'SUPPRESSED').length;

  document.getElementById('count-all').textContent = allCount;
  document.getElementById('count-mosca').textContent = moscaCount;
  document.getElementById('count-actionable').textContent = actionableCount;
  document.getElementById('count-suppressed').textContent = suppressedCount;
}

// ==========================================
// Inventory Table & Search
// ==========================================

function initSearchAndFilters() {
  const searchInput = document.getElementById('inventory-search');
  const chips = document.querySelectorAll('.filter-chips .chip');

  searchInput.addEventListener('input', () => {
    applyFilterAndSearch();
  });

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilter = chip.getAttribute('data-filter');
      applyFilterAndSearch();
    });
  });

  document.getElementById('btn-export-cbom-quick').addEventListener('click', () => {
    downloadCBOM();
  });
}

function applyFilterAndSearch() {
  if (!currentScanData || !currentScanData.findings) return;
  const query = document.getElementById('inventory-search').value.toLowerCase().trim();

  const filtered = currentScanData.findings.filter(f => {
    // Filter chip
    if (currentFilter === 'mosca' && !f.moscaViolated) return false;
    if (currentFilter === 'actionable' && !f.isSecurityRelevant) return false;
    if (currentFilter === 'suppressed' && f.urgencyTier !== 'SUPPRESSED') return false;

    // Search query
    if (query) {
      const match = (
        f.algorithm.toLowerCase().includes(query) ||
        f.fileName.toLowerCase().includes(query) ||
        f.plaintextSource.toLowerCase().includes(query) ||
        f.ciphertextSink.toLowerCase().includes(query) ||
        f.urgencyTier.toLowerCase().includes(query)
      );
      if (!match) return false;
    }
    return true;
  });

  renderInventoryTable(filtered);
}

function renderInventoryTable(findings) {
  const tbody = document.getElementById('inventory-tbody');
  tbody.innerHTML = '';

  if (findings.length === 0) {
    tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; color:var(--text-dim); padding:2rem;">No cryptographic invocations match the selected filter.</td></tr>`;
    return;
  }

  findings.forEach(f => {
    const tr = document.createElement('tr');

    // Rank badge
    const rankClass = f.rank === 1 ? 'rank-badge top-rank' : 'rank-badge';

    // Retention string
    let retStr = `${f.retentionYears.toFixed(1)}y`;
    if (f.retentionYears < 0.01) retStr = '<1h';
    else if (f.retentionYears < 1.0) retStr = `${Math.round(f.retentionYears * 365)}d`;

    // Urgency badge
    let badgeClass = 'badge-low';
    let statusText = f.urgencyTier;
    if (f.moscaViolated) {
      badgeClass = 'badge-critical';
      statusText = '🚨 MOSCA BREACH';
    } else if (f.urgencyTier === 'HIGH') {
      badgeClass = 'badge-high';
    } else if (f.urgencyTier === 'MEDIUM') {
      badgeClass = 'badge-medium';
    } else if (f.urgencyTier === 'SUPPRESSED') {
      badgeClass = 'badge-suppressed';
    }

    // Score bar color
    let barColor = 'var(--text-dim)';
    if (f.hndlScore >= 20.0) barColor = 'var(--breach-text)';
    else if (f.hndlScore >= 10.0) barColor = 'var(--danger-text)';
    else if (f.hndlScore >= 1.0) barColor = 'var(--warning-text)';
    else if (f.isSecurityRelevant) barColor = 'var(--success-text)';

    tr.innerHTML = `
      <td><span class="${rankClass}">${f.rank}</span></td>
      <td class="algo-cell">
        <strong>${escapeHtml(f.algorithm)}</strong>
        ${f.keySize ? `<br><small style="color:var(--text-dim)">${f.keySize} bits</small>` : ''}
      </td>
      <td class="location-cell">
        <span style="color:var(--primary); font-weight:500;">${escapeHtml(f.fileName)}</span>:${f.lineNumber}
      </td>
      <td><code>${escapeHtml(f.plaintextSource)}</code></td>
      <td><code>${escapeHtml(f.ciphertextSink)}</code></td>
      <td><strong>${retStr}</strong></td>
      <td><small>${escapeHtml(f.exposureSurface)}</small></td>
      <td>
        <div class="score-bar-wrapper">
          <span class="score-val">${f.hndlScore.toFixed(1)}</span>
          <div class="score-track">
            <div class="score-fill" style="width:${Math.min(100, f.hndlScore * 3)}%; background:${barColor};"></div>
          </div>
        </div>
      </td>
      <td><span class="badge-status ${badgeClass}">${statusText}</span></td>
      <td>
        <button class="btn btn-sm btn-outline view-btn" data-rank="${f.rank}">Inspect</button>
      </td>
    `;

    tr.querySelector('.view-btn').addEventListener('click', () => {
      openDetailModal(f);
    });

    tbody.appendChild(tr);
  });
}

// ==========================================
// Dataflow Visualizer
// ==========================================

function renderDataflowDiagrams(findings) {
  const container = document.getElementById('dataflow-visual-container');
  container.innerHTML = '';

  findings.forEach(f => {
    const card = document.createElement('div');
    card.className = `dataflow-card ${f.moscaViolated ? 'card-breach' : ''}`;

    let badgeClass = f.moscaViolated ? 'badge-critical' : (f.isSecurityRelevant ? 'badge-info' : 'badge-suppressed');
    let statusText = f.moscaViolated ? 'MOSCA VIOLATION ($x+y>z$)' : (f.isSecurityRelevant ? 'Active Dataflow' : 'Noise Suppressed');

    let retStr = `${f.retentionYears.toFixed(1)}y (${f.retentionEvidenceType})`;
    if (f.retentionYears < 0.01) retStr = '< 15 mins (Redis TTL)';

    card.innerHTML = `
      <div class="dataflow-header">
        <div class="dataflow-title">
          <span class="rank-badge ${f.rank === 1 ? 'top-rank' : ''}">${f.rank}</span>
          <strong>${escapeHtml(f.fileName)}:${f.lineNumber} — ${escapeHtml(f.algorithm)}</strong>
        </div>
        <span class="badge-status ${badgeClass}">${statusText}</span>
      </div>

      <div class="dataflow-diagram">
        <div class="flow-node">
          <div class="node-label">Plaintext Source</div>
          <div class="node-value">${escapeHtml(f.plaintextSource)}</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node" style="border-color:var(--primary); background:var(--primary-glow);">
          <div class="node-label">Transformation</div>
          <div class="node-value" style="color:var(--primary);">${escapeHtml(f.algorithm)}</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node">
          <div class="node-label">Ciphertext Sink</div>
          <div class="node-value">${escapeHtml(f.ciphertextSink)}</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node">
          <div class="node-label">Lifecycle Retention ($x$)</div>
          <div class="node-value">${retStr}</div>
        </div>
      </div>

      <div class="dataflow-footer">
        <div><strong>Exposure Surface:</strong> ${escapeHtml(f.exposureSurface)} (Factor: ${f.exposureFactor})</div>
        <div><strong>Remediation:</strong> ${escapeHtml(f.recommendation)}</div>
      </div>
    `;

    container.appendChild(card);
  });
}

// ==========================================
// Mosca's Simulator
// ==========================================

function initMoscaSimulator() {
  const sliderX = document.getElementById('slider-x');
  const sliderY = document.getElementById('slider-y');
  const sliderZ = document.getElementById('slider-z');
  const selExposure = document.getElementById('select-exposure');
  const selVuln = document.getElementById('select-vuln');

  const updateSim = async () => {
    const x = parseFloat(sliderX.value);
    const y = parseFloat(sliderY.value);
    const z = parseFloat(sliderZ.value);
    const exposure = selExposure.value;
    const vuln = selVuln.value;

    document.getElementById('val-x').textContent = `${x.toFixed(1)} years`;
    document.getElementById('val-y').textContent = `${y.toFixed(1)} years`;
    document.getElementById('val-z').textContent = `${z.toFixed(1)} years`;

    document.getElementById('eq-x').textContent = x.toFixed(1);
    document.getElementById('eq-y').textContent = y.toFixed(1);
    document.getElementById('eq-z').textContent = z.toFixed(1);
    document.getElementById('eq-sum').textContent = `${(x + y).toFixed(1)}y`;

    try {
      const res = await fetch('/api/simulate-mosca', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          retentionYears: x,
          migrationYears: y,
          crqcHorizonYears: z,
          exposureSurface: exposure,
          quantumVulnerability: vuln,
          keyReuseCount: 1
        })
      });
      const data = await res.json();
      renderSimResults(data.score, x + y > z);
    } catch (err) {
      // Local computation fallback
      const violated = (x + y) > z;
      const exposureWeight = { EXTERNAL_PUBLIC: 1.0, EXTERNAL_PARTNER: 0.75, INTERNAL_CROSS_HOST: 0.5, INTERNAL_IPC: 0.25, IN_PROCESS: 0.1 }[exposure] || 1.0;
      const algWeight = { SHOR_BROKEN: 1.0, GROVER_WEAKENED: 0.3, QUANTUM_SAFE: 0.05 }[vuln] || 1.0;
      const retFactor = Math.min(30.0, x) / 30.0;
      const raw = retFactor * exposureWeight * algWeight;
      const scoreNum = Math.min(100.0, raw * 100.0);
      renderSimResults({
        normalizedScore: scoreNum,
        urgencyTier: violated && scoreNum >= 20 ? 'CRITICAL_IMMEDIATE' : (scoreNum >= 10 ? 'HIGH' : (scoreNum >= 1 ? 'MEDIUM' : 'LOW')),
        moscaViolated: violated,
        recommendation: violated ? `Mosca's inequality violated (${(x+y).toFixed(1)}y > ${z.toFixed(1)}y). Immediate hybrid FIPS 203 (ML-KEM) migration required.` : 'Data confidentiality lifetime expires safely prior to CRQC horizon.',
        factors: { retention: retFactor, exposure: exposureWeight, algorithm: algWeight, keyReuse: 1.0 }
      }, violated);
    }
  };

  sliderX.addEventListener('input', updateSim);
  sliderY.addEventListener('input', updateSim);
  sliderZ.addEventListener('input', updateSim);
  selExposure.addEventListener('change', updateSim);
  selVuln.addEventListener('change', updateSim);

  updateSim();
}

function renderSimResults(score, violated) {
  const badge = document.getElementById('sim-status-badge');
  const scoreNum = document.getElementById('sim-score-num');
  const tier = document.getElementById('sim-urgency-tier');
  const rec = document.getElementById('sim-rec-text');

  scoreNum.textContent = score.normalizedScore.toFixed(1);
  tier.textContent = score.urgencyTier;
  rec.textContent = score.recommendation;

  if (score.moscaViolated || violated) {
    badge.className = 'badge-status badge-critical';
    badge.textContent = '🚨 MOSCA VIOLATION';
    tier.style.color = 'var(--breach-text)';
  } else {
    badge.className = 'badge-status badge-info';
    badge.textContent = 'SECURE HORIZON';
    tier.style.color = 'var(--accent-emerald)';
  }

  document.getElementById('factor-r').textContent = (score.factors?.retention || 0).toFixed(4);
  document.getElementById('factor-e').textContent = (score.factors?.exposure || 0).toFixed(2);
  document.getElementById('factor-a').textContent = (score.factors?.algorithm || 0).toFixed(2);
  document.getElementById('factor-k').textContent = (score.factors?.keyReuse || 1.0).toFixed(2);
}

// ==========================================
// Live Code Scanner
// ==========================================

function initCodeScanner() {
  const textarea = document.getElementById('code-input');
  const runBtn = document.getElementById('btn-run-code-scan');
  const statusTag = document.getElementById('scan-status-tag');
  const resultsContainer = document.getElementById('code-scan-results');
  const presetBtns = document.querySelectorAll('.preset-btn');

  // Preload preset
  textarea.value = PRESETS.archive;

  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      presetBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const key = btn.getAttribute('data-preset');
      if (PRESETS[key]) {
        textarea.value = PRESETS[key];
        runCodeScan();
      }
    });
  });

  runBtn.addEventListener('click', runCodeScan);

  async function runCodeScan() {
    const code = textarea.value.trim();
    if (!code) return;

    statusTag.className = 'badge-status badge-info';
    statusTag.textContent = 'Analyzing AST...';

    try {
      const res = await fetch('/api/scan-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code, filename: 'custom_snippet.py' })
      });
      const data = await res.json();
      renderScanSnippetResults(data);
      statusTag.className = 'badge-status badge-info';
      statusTag.textContent = 'Scan Complete';
    } catch (err) {
      statusTag.className = 'badge-status badge-critical';
      statusTag.textContent = 'Scan Error';
      resultsContainer.innerHTML = `<div style="color:var(--danger-text); padding:1rem;">Analysis failed: ${escapeHtml(err.message)}</div>`;
    }
  }
}

function renderScanSnippetResults(data) {
  const container = document.getElementById('code-scan-results');
  if (!data.findings || data.findings.length === 0) {
    container.innerHTML = `<div class="empty-state">No cryptographic primitives discovered in code snippet.</div>`;
    return;
  }

  let html = '';
  data.findings.forEach(f => {
    let badgeClass = f.moscaViolated ? 'badge-critical' : (f.isSecurityRelevant ? 'badge-info' : 'badge-suppressed');
    let statusText = f.moscaViolated ? 'MOSCA BREACH' : f.urgencyTier;

    html += `
      <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:var(--radius-md); padding:1rem; display:flex; flex-direction:column; gap:0.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong style="color:var(--primary); font-size:1rem;">${escapeHtml(f.algorithm)}</strong>
          <span class="badge-status ${badgeClass}">${statusText}</span>
        </div>
        <div style="font-size:0.8rem; color:var(--text-muted);">
          Line ${f.lineNumber} · Type: ${f.primitiveType} · Quantum Vuln: ${f.quantumVulnerability}
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; font-size:0.8rem; margin-top:0.5rem; background:var(--bg-secondary); padding:0.75rem; border-radius:var(--radius-sm);">
          <div><strong>Plaintext Source:</strong> ${escapeHtml(f.plaintextSource)}</div>
          <div><strong>Ciphertext Sink:</strong> ${escapeHtml(f.ciphertextSink)}</div>
          <div><strong>Retention:</strong> ${f.retentionYears.toFixed(1)}y</div>
          <div><strong>Exposure Surface:</strong> ${escapeHtml(f.exposureSurface)}</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem; padding-top:0.5rem; border-top:1px solid var(--border-color);">
          <span style="font-weight:700;">HNDL Exposure Score: <span style="color:var(--primary);">${f.hndlScore.toFixed(1)} / 100</span></span>
          <span style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(f.recommendation)}</span>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

// ==========================================
// CycloneDX 1.6 CBOM Tab & Actions
// ==========================================

function initCBOMActions() {
  document.getElementById('btn-copy-cbom').addEventListener('click', () => {
    const code = document.getElementById('cbom-json-content').textContent;
    navigator.clipboard.writeText(code).then(() => {
      const btn = document.getElementById('btn-copy-cbom');
      btn.textContent = '✅ Copied!';
      setTimeout(() => { btn.textContent = '📋 Copy JSON'; }, 2000);
    });
  });

  document.getElementById('btn-download-cbom').addEventListener('click', () => {
    downloadCBOM();
  });
}

function renderCBOM(cbomDoc) {
  const container = document.getElementById('cbom-json-content');
  if (cbomDoc) {
    container.textContent = JSON.stringify(cbomDoc, null, 2);
  }
}

function downloadCBOM() {
  if (!currentScanData || !currentScanData.cbom) return;
  const jsonStr = JSON.stringify(currentScanData.cbom, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `cyclonedx-1.6-cbom-${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// ==========================================
// Detail Modal
// ==========================================

function openDetailModal(f) {
  const modal = document.getElementById('detail-modal');
  const title = document.getElementById('modal-title');
  const body = document.getElementById('modal-body');

  title.textContent = `${f.algorithm} Invocation Details (Rank #${f.rank})`;

  body.innerHTML = `
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
      <div><strong>File Location:</strong><br><code>${escapeHtml(f.filePath)}:${f.lineNumber}</code></div>
      <div><strong>Urgency Status:</strong><br><span class="badge-status ${f.moscaViolated ? 'badge-critical' : 'badge-info'}">${f.urgencyTier}</span></div>
      <div><strong>Plaintext Source:</strong><br><code>${escapeHtml(f.plaintextSource)}</code></div>
      <div><strong>Ciphertext Sink:</strong><br><code>${escapeHtml(f.ciphertextSink)}</code></div>
      <div><strong>Retention Duration:</strong><br>${f.retentionYears.toFixed(1)} years (${f.retentionEvidenceType})</div>
      <div><strong>Exposure Surface:</strong><br>${escapeHtml(f.exposureSurface)} (Factor: ${f.exposureFactor})</div>
      <div><strong>HNDL Score:</strong><br><strong style="color:var(--primary); font-size:1.2rem;">${f.hndlScore.toFixed(1)} / 100</strong></div>
      <div><strong>Mosca's Inequality:</strong><br>${f.moscaViolated ? '<span style="color:var(--breach-text); font-weight:bold;">VIOLATED ($x+y>z$)</span>' : 'SATISFIED ($x+y\\leq z$)'}</div>
    </div>

    <div style="margin-top:0.5rem;">
      <strong>Remediation Directive:</strong>
      <p style="background:var(--bg-primary); padding:0.75rem; border-radius:var(--radius-sm); border:1px solid var(--border-color); font-size:0.85rem; margin-top:0.25rem;">
        ${escapeHtml(f.recommendation)}
      </p>
    </div>

    <div style="margin-top:0.5rem;">
      <strong>Extracted Code Snippet:</strong>
      <pre style="background:var(--bg-primary); padding:0.75rem; border-radius:var(--radius-sm); border:1px solid var(--border-color); font-family:var(--font-mono); font-size:0.8rem; overflow-x:auto; margin-top:0.25rem; color:#a5b4fc;"><code>${escapeHtml(f.rawCodeSnippet || '# No raw snippet attached')}</code></pre>
    </div>
  `;

  modal.classList.remove('hidden');

  document.getElementById('modal-close').onclick = () => {
    modal.classList.add('hidden');
  };
  modal.onclick = (e) => {
    if (e.target === modal) modal.classList.add('hidden');
  };
}

// ==========================================
// Utilities
// ==========================================

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function renderFallbackData() {
  const fallback = {
    metrics: {
      totalFindings: 3,
      actionableCount: 2,
      suppressedCount: 1,
      noiseFilteredPercent: 33.3,
      moscaBreaches: 1,
      shorBrokenCount: 2,
      averageActionableScore: 11.5
    },
    targetName: "examples/sample_project",
    findings: [
      {
        rank: 1,
        algorithm: "RSA-OAEP",
        primitiveType: "asymmetric_encryption",
        keySize: 2048,
        quantumVulnerability: "SHOR_BROKEN",
        filePath: "examples/sample_project/payments/archive.py",
        fileName: "archive.py",
        lineNumber: 19,
        rawCodeSnippet: "ciphertext = rsa_public_key.encrypt(record_bytes, padding.OAEP(...))",
        plaintextSource: "database_read",
        ciphertextSink: "cloud_object_store",
        retentionYears: 10.0,
        retentionEvidenceType: "s3_lifecycle_policy",
        retentionObserved: true,
        exposureSurface: "EXTERNAL_PUBLIC",
        exposureFactor: 1.0,
        hndlScore: 23.0,
        urgencyTier: "CRITICAL_IMMEDIATE",
        moscaViolated: true,
        recommendation: "Mosca's inequality violated (10y retention + 2y migration > 7y CRQC horizon). Immediate migration to hybrid FIPS 203 (ML-KEM) required.",
        isSecurityRelevant: true
      },
      {
        rank: 2,
        algorithm: "RSA-OAEP",
        primitiveType: "asymmetric_encryption",
        keySize: 2048,
        quantumVulnerability: "SHOR_BROKEN",
        filePath: "examples/sample_project/web/session.py",
        fileName: "session.py",
        lineNumber: 18,
        rawCodeSnippet: "enc_token = rsa_public_key.encrypt(token_data, padding.OAEP(...))",
        plaintextSource: "local_rng_token",
        ciphertextSink: "in_memory_cache",
        retentionYears: 0.00003,
        retentionEvidenceType: "redis_ttl",
        retentionObserved: true,
        exposureSurface: "EXTERNAL_PUBLIC",
        exposureFactor: 1.0,
        hndlScore: 0.0,
        urgencyTier: "LOW",
        moscaViolated: false,
        recommendation: "Low exposure or short-lived data. Defer migration.",
        isSecurityRelevant: true
      },
      {
        rank: 3,
        algorithm: "SHA-256",
        primitiveType: "hash",
        keySize: null,
        quantumVulnerability: "GROVER_WEAKENED",
        filePath: "examples/sample_project/cache/etags.py",
        fileName: "etags.py",
        lineNumber: 14,
        rawCodeSnippet: "hasher = hashlib.sha256()",
        plaintextSource: "computed_digest",
        ciphertextSink: "network_response",
        retentionYears: 0.0,
        retentionEvidenceType: "etag_digest",
        retentionObserved: true,
        exposureSurface: "EXTERNAL_PUBLIC",
        exposureFactor: 1.0,
        hndlScore: 0.0,
        urgencyTier: "SUPPRESSED",
        moscaViolated: false,
        recommendation: "Suppressed: Non-security context",
        isSecurityRelevant: false
      }
    ],
    cbom: {
      bomFormat: "CycloneDX",
      specVersion: "1.6",
      components: []
    }
  };
  currentScanData = fallback;
  renderAll(fallback);
}
