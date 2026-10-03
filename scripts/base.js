/**
 * Generates Crypto-Agility_Navigator_Review2.pptx
 * Matches the exact styling, color palette, dark theme, and typography of Review 1
 * Aligned strictly with BACSE291 IDP Review II evaluation rubrics (20 Marks).
 */

const path = require('path');
const pptxgen = require('pptxgenjs');

const pres = new pptxgen();

pres.layout = 'LAYOUT_16x9'; // 10 x 5.625 inches

// Color Palette matching Review 1
const BG_DARK = 'FFFFFF';
const CARD_BG = 'F8F9FA';
const BORDER_COLOR = 'E0E0E0';
const TEXT_MUTED = '666666';
const TEXT_BODY = '333333';
const TEXT_WHITE = '000000';
const ACCENT_RED = 'D32F2F';
const ACCENT_GREEN = '2E7D32';
const ACCENT_BLUE = '1976D2';

const TOTAL_SLIDES = 37;

function addSlideBase(pres, slideNum, sectionName, title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: BG_DARK };

  // Header line
  slide.addShape(pres.ShapeType.line, {
    x: 0.5, y: 0.68, w: 9.0, h: 0,
    line: { color: BORDER_COLOR, width: 1 }
  });

  // Top header text
  slide.addText('CRYPTO-AGILITY NAVIGATOR', {
    x: 0.5, y: 0.35, w: 5.5, h: 0.25,
    fontSize: 9, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 1.5
  });

  slide.addText(sectionName.toUpperCase(), {
    x: 5.0, y: 0.35, w: 4.5, h: 0.25,
    fontSize: 9, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true, tracking: 1.5
  });

  // Title & Subtitle
  slide.addText(title, {
    x: 0.5, y: 0.85, w: 9.0, h: 0.3,
    fontSize: 12, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 1.2
  });

  slide.addText(subtitle, {
    x: 0.5, y: 1.15, w: 9.0, h: 0.45,
    fontSize: 18, fontFace: 'Arial', color: TEXT_WHITE, bold: true
  });

  // Footer divider line
  slide.addShape(pres.ShapeType.line, {
    x: 0.5, y: 5.15, w: 9.0, h: 0,
    line: { color: BORDER_COLOR, width: 1 }
  });

  // Footer text
  slide.addText(sectionName.toUpperCase(), {
    x: 0.5, y: 5.25, w: 6.5, h: 0.25,
    fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, bold: true
  });

  const numStr = `${String(slideNum).padStart(2, '0')} / ${TOTAL_SLIDES}`;
  slide.addText(numStr, {
    x: 7.5, y: 5.25, w: 2.0, h: 0.25,
    fontSize: 8.5, fontFace: 'Arial', color: TEXT_MUTED, align: 'right', bold: true
  });

  return slide;
}

// -------------------------------------------------------------
// SLIDE 1: Title Slide
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  slide.background = { color: BG_DARK };

  slide.addText('REVIEW REPORT II · INNOVATIVE DESIGN PROJECT (BACSE291)', {
    x: 0.8, y: 1.2, w: 8.4, h: 0.35,
    fontSize: 11, fontFace: 'Arial', color: TEXT_MUTED, bold: true, tracking: 2
  });

  slide.addText('Crypto-Agility Navigator', {
    x: 0.8, y: 1.6, w: 8.4, h: 0.9,
    fontSize: 34, fontFace: 'Arial', color: TEXT_WHITE, bold: true
  });

  slide.addText('Dataflow-Aware Cryptographic Inventory & Prioritised Post-Quantum Migration', {
    x: 0.8, y: 2.5, w: 8.4, h: 0.45,
    fontSize: 15, fontFace: 'Arial', color: TEXT_BODY
  });

  // Metadata Card
  slide.addShape(pres.ShapeType.rect, {
    x: 0.8, y: 3.2, w: 8.4, h: 1.5,
    fill: { color: CARD_BG },
    line: { color: BORDER_COLOR, width: 1 }
  });

  slide.addText([
    { text: 'EVALUATION MILESTONE: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Review II — Initial Design and Development (20 Marks)\n', options: { color: TEXT_BODY } },
    { text: 'ASSESSMENT FOCUS: ', options: { bold: true, color: TEXT_WHITE } },
    { text: '~20% Completion · Architecture · Tool Justification · TRL 3 Working Prototype\n', options: { color: TEXT_BODY } },
    { text: 'TEAM & ACADEMIC YEAR: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'Team of 3 Students · Academic Year 2026–2027 · Software-Only Track (No Specialized Hardware)\n', options: { color: TEXT_BODY } },
    { text: 'KEY STANDARDS: ', options: { bold: true, color: TEXT_WHITE } },
    { text: 'OWASP CycloneDX 1.6 CBOM · NIST FIPS 203/204/205 · Open Quantum Safe (liboqs)', options: { color: TEXT_MUTED } }
  ], {
    x: 1.1, y: 3.35, w: 7.8, h: 1.2,
    fontSize: 9.5, fontFace: 'Arial', lineSpacing: 16
  });

  slide.addText(`01 / ${TOTAL_SLIDES}`, {
