#include <map>
#include <vector>
#include <iostream>
#include <algorithm>
#include <iterator>

using std::vector;
using std::pair;

using std::cout;
using std::cin;
using std::endl;

const int FLDSIZE = 3;
const int X_MARK = 1;
const int O_MARK = -1;
const char X_SYM = 'x';
const char O_SYM = 'o';


pair<int, int> turn(const vector<char> & field, const vector<int> & moves){
	int best = 0;
	for (int i = 0; i < moves.size(); i++){
		if (field[moves[i]] != X_SYM && field[moves[i]] != O_SYM){
			best = moves[i];
			break;
		}
	}
			
	return std::make_pair(best/FLDSIZE, best%FLDSIZE);
}

int main(){
	//read inp field
	vector<int> moves_order(9);
//center
	moves_order[0] = 4;
//corners
	moves_order[1] = 0;
	moves_order[2] = 2;
	moves_order[3] = 6;
	moves_order[4] = 8;
//middles
	moves_order[5] = 1;
	moves_order[6] = 3;
	moves_order[7] = 5;
	moves_order[8] = 7;

	vector<char> field(9);

	for (int i = 0; i != 9; ++i){
	    cin >> field[i];
	}
	
    //analyse field

	pair<int, int> pos = turn(field, moves_order);
	//output move
	cout << pos.first << ' ' << pos.second<<endl;

	return 0;
}
