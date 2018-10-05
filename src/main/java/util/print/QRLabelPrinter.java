package util.print;

import javax.print.attribute.HashPrintRequestAttributeSet;
import javax.print.attribute.PrintRequestAttributeSet;

import java.awt.image.BufferedImage;
import java.awt.print.*;
import java.awt.*;

public class QRLabelPrinter {

    public static void print(BufferedImage qrCodeImage) {
        System.out.println("Printing QR code label...");
        PrinterJob job = PrinterJob.getPrinterJob();
        PrintRequestAttributeSet attributeSet = new HashPrintRequestAttributeSet();

        job.setJobName("QR Code Label Print");

        job.setPrintable((graphics, pageFormat, pageIndex) -> {
            if (pageIndex !=0) {
                return Printable.NO_SUCH_PAGE;
            }
            graphics.drawImage(qrCodeImage, (int) pageFormat.getImageableX(), (int) pageFormat.getImageableY(),
                    qrCodeImage.getWidth(), qrCodeImage.getHeight(), null);
            return Printable.PAGE_EXISTS;
        });
        boolean doPrint = job.printDialog();

        if (doPrint) {
            try {
                job.print();
            } catch (PrinterException e) {
                // The job did not successfully complete
                System.out.println("Print failed. Job: " + job.toString());
            }
        }
    }
}
