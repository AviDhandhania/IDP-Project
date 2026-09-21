package examples.sample_project.payments;

import javax.crypto.Cipher;
import java.security.PublicKey;
import com.amazonaws.services.s3.AmazonS3;

public class JavaArchive {
    public boolean processArchive(byte[] record, PublicKey pubKey, AmazonS3 s3Client) throws Exception {
        String cipherAlgo = "RSA/ECB/OAEPWithSHA-256AndMGF1Padding";
        
        // cryptographic invocation
        Cipher cipher = Cipher.getInstance(cipherAlgo);
        cipher.init(Cipher.ENCRYPT_MODE, pubKey);
        byte[] blob = cipher.doFinal(record);
        
        // retention: 10 years
        s3Client.putObject("settlements-archive", "java_audit.enc", new String(blob));
        return true;
    }
}
