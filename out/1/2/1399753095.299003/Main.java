package ru.spbau.kalakutsky.task01;

/**
 * Class for task01.
 * <p>
 * Calculates and prints sum of numbers given like command arguments.
 * Arguments must be valid numbers and may be separated by
 * whitespace characters
 *
 * @author  Arkady Kalakutsky
 *
 * Date: 2/22/14
 * Time: 8:15 PM
 */
public class Sum {
    /**
     * Converts input string to integer number.
     * @param src string to convert
     * @return    integer from string.
     */
    public static int stringToInt(String src){
        int res = 0;
        int i = 0;
        boolean minus = false;
        if (src.charAt(0)=='-'){
            minus = true;
            i++;
        }

        for(; i < src.length(); i++){
            res = res*10 + src.charAt(i) - '0';
        }
        if (minus){
            res = -res;
        }
        return res;
    }

    /**
     * main method where strings are converted and numbers are summed up
     * @param args  command-line arguments, consisting of integers
     */
    public static void main(String[] args){
        int sum = 0;
        for(String arg:args){
            for (String number:arg.trim().split("\\s+")){
                    sum += stringToInt(number);
            }
        }
        System.out.printf("Результат: %d\n", sum);
    }
}
