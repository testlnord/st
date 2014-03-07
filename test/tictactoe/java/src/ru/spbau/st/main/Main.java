package ru.spbau.st.main;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {

	private static int mark = 1;

	public static int[][] field = new int[3][3];

	public static void main(String[] arg) throws IOException {
		readInput();
		makeTurn();
		print();

	}

	private static void readInput() throws IOException {
		String input;
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		input = in.readLine();

		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				switch (input.charAt(i + j)) {
				case 'x':
					field[i][j] = 1;
					break;
				case 'o':
					field[i][j] = -1;
					break;
				default:
					field[i][j] = 0;
					break;
				}
			}
		}

		if (sum() > 0) {
			mark = -1;
		} else {
			mark = 1;
		}

	}

	private static void makeTurn() {
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				if (field[i][j] == 0) {
					field[i][j] = mark;
					return;
				}
			}
		}
	}

	private static int sum() {
		int sum = 0;
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				sum += field[i][j];
			}
		}
		return sum;
	}

	// private int checkStatement() {
	// return 0;
	// }
	//
	// private int checkWinTurn() {
	// return 0;
	// }
	//
	// private int checkEnemyWinTurn() {
	// return 0;
	// }

	private static void print() {
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				switch (field[i][j]) {
				case 1:
					System.out.print('x');
					break;
				case -1:
					System.out.print('o');
					break;
				default:
					System.out.print('L');
					break;
				}
			}
		}
	}
}
