package util.qr;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;

import java.io.File;
import java.io.IOException;

import java.text.SimpleDateFormat;

import java.util.Date;
import java.util.Hashtable;

import javax.imageio.ImageIO;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.EncodeHintType;
import com.google.zxing.WriterException;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;

public class QRCodeEncoder {

    public static void main(String[] args) throws WriterException, IOException {
        String text = "testing";
        int size = 250;
        String fileType = "png";
        generate(text, size, fileType);
        System.out.println("Encoding complete.");
    }

    public static BufferedImage generate(String text, int size, String fileType)
            throws WriterException, IOException {
        File qrFile = new File(new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date())
                        + "."
                        + fileType);

        //Create the BitMatrix for the QRCode that encodes the given String
        Hashtable<EncodeHintType, ErrorCorrectionLevel> hintMap = new Hashtable<>();
        hintMap.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.L);
        QRCodeWriter qrCodeWriter = new QRCodeWriter();
        BitMatrix bitMatrix = qrCodeWriter.encode(text, BarcodeFormat.QR_CODE, size, size, hintMap);

        // Make the BufferedImage that holds the QRCode
        int matrixSideLength = bitMatrix.getWidth();
        BufferedImage image = new BufferedImage(matrixSideLength, matrixSideLength, BufferedImage.TYPE_INT_RGB);
        image.createGraphics();

        Graphics2D graphics = (Graphics2D) image.getGraphics();
        graphics.setColor(Color.WHITE);
        graphics.fillRect(0,0, matrixSideLength, matrixSideLength);
        // Paint and save the image using the BitMatrix;
        graphics.setColor(Color.BLACK);

        for (int i = 0; i < matrixSideLength; i++) {
            for (int j = 0; j < matrixSideLength; j++) {
                if (bitMatrix.get(i, j)) {
                    graphics.fillRect(i, j, 1, 1);
                }
            }
        }

        ImageIO.write(image, fileType, qrFile);
        return image;
    }
}
