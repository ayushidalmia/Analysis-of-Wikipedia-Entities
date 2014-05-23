import edu.jhu.nlp.wikipedia.*;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class parseFull
{
    static int i=0;;
    public static void main(String args[])
    {
        i=0;
        int count=0;
        String inputDirectory=args[0];

        int numberOfFiles=new File(inputDirectory).listFiles().length;
        for(i=1;i<=numberOfFiles;i++)
        {
            String inputFile=inputDirectory.concat("page"+i+".xml");
            WikiXMLParser wxsp = WikiXMLParserFactory.getSAXParser(inputFile);
            try 
            {  
                wxsp.setPageCallback(new PageCallbackHandler() { 
                   public void process(WikiPage page) {

                        String infobox=page.getInfoBox().dumpRaw();
                        infobox=infobox.substring(2,infobox.length()-2);
                        try
                        {
                            
                            String outputFileName="H:\\MS\\Web Mining\\Assignment\\Assignment 4\\Data\\Sample InfoBoxes/";
                            outputFileName=outputFileName.concat("page"+i+".txt");
                            final FileWriter outputFileWriter = new FileWriter(new File(outputFileName));
                            final BufferedWriter bw = new BufferedWriter(outputFileWriter);
                            System.out.println(i);
                            bw.write(infobox);
                            bw.close();
                        }catch(IOException io)
                        {
                            io.printStackTrace();
                        }
                   }
                });
                wxsp.parse();
            }catch(Exception e) 
            {
              continue;
            }
        }
        //System.out.println(count);
    }
}
