import javax.swing.*;
import java.io.File;
import java.io.IOException;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

public class FileTreatment {
  private String fileName;
  private File file;
  private String filePath;

  public void openPDF() {
    JFileChooser chooser = new JFileChooser();
    chooser.setDialogTitle("Selecione o arquivo PDF");
    int result = chooser.showOpenDialog(null);

    if (result == JFileChooser.APPROVE_OPTION) {
      this.file = chooser.getSelectedFile();
      this.fileName = file.getName();
      this.filePath = file.getAbsolutePath();

      if (!fileName.toLowerCase().endsWith(".pdf")) {
        JOptionPane.showMessageDialog(null, "Selecione um arquivo PDF válido.");
        return;
      }

      try (PDDocument pdfDocument = Loader.loadPDF(this.file)) {
        PDFTextStripper stripper = new PDFTextStripper();
        String filetext = stripper.getText(pdfDocument);

        // Teste
        System.out.println("Conteúdo extraído (primeiras 300 letras):");
        System.out.println(filetext.substring(0, Math.min(300, filetext.length())));

      } catch (IOException e) {
        JOptionPane.showMessageDialog(null, "Erro ao abrir o PDF: " + e.getMessage());
        e.printStackTrace();
      }
    }
  }
}
