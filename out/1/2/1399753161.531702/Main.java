package ru.spbau.kalakutsky.task02;

import java.io.FileNotFoundException;
import java.io.IOException;


/**
 * Tests message and all message reader/writers.
 * Read messages from input file and writes them, compressed, to output file
 * if specified, or console.
 * @author arkady
 */
public class Main {
    /**
     * Entry point of programm.
     * @param args args[0] - input file, args[1] - output file (optional)
     */
    public static void main(String[] args){

        if (args.length != 1 && args.length != 2){
            System.out.println("Usage: main <input file> [<output file>]");
            return;
        }


        try ( FileMessageReader fileMessageReader = new FileMessageReader(args[0]);
              CompressingMessageWrite compressingMessageWrite =
                      new CompressingMessageWrite(
                              args.length == 1 ?
                                      new ConsoleMessageWriter() :
                                      new FileMessageWriter(args[1])
                      )
        )  {

            Message message;
            while ((message = fileMessageReader.readMessage()) != null){
                compressingMessageWrite.writeMessage(message);
            }

        }catch (IllegalMessageFormatException e){
            System.err.printf("Wrong message format. Wrong or corrupted input file. %s\n", e.getMessage());
        } catch (FileNotFoundException e) {
            System.err.printf("Input file %s not found.\n", args[0]);
        } catch (IOException e) {
            System.err.printf("Read/write error occurred. \nMessage: %s\n", e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.printf("Strange exception occurred. \nMessage: %s\n", e.getMessage());
            e.printStackTrace();
        }

    }
}
