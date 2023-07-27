#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

static int rounds{}, player{}, computer{};

//Thsis gives the game introduction and starts the game
void game_intro()
{
    cout << "Rock-Paper-Scissor Game" << endl;
    cout << "Enter the number of turns to play: ";
    cin >> rounds;
}

//This is the brain of the game which compares the moves and gives the result
int game_func(int p1, int p2)
{
    int gam_ary[] = {1, 2, 3, 1};
    if(p1 == p2) return 0;
    if(p2 == gam_ary[p1]) return -1;
    else return 1;
}

//This display_moves the moves i.e., converts numbers 1,2,3 to Rock, Paper & scissor
void display_move(int i)
{
    if(i == 1) cout << "Rock" << endl;
    else if(i == 2) cout << "Paper" << endl;
    else cout << "Scissor" << endl;
}

//This takes input from the player -- The function is implemented so that the game recieves valid input from the player
int take_input()
{
    int input{};
    while(1)
    {
        cin >> input;
        if(input > 0 and input < 4) break;
        else
        {
            cout << "Invalid input" << endl;
            cout << "Move: ";
        }
    }
    return input;
}


//The function handles the game play
//It takes moves, calculates the result and shows the result of each match
void game_play()
{
    srand(time(nullptr));
    int p1{}, comp{}, res{};
    for(int i = 0; i<rounds; i++)
    {
        cout << "Make your move: " << endl;
        cout << "1-Rock 2-Paper 3-Scissor" << endl;

        cout << "Move: ";
        p1 = take_input();
        cout << "You played: ";
        display_move(p1);

        comp = (rand()%3)+1;
        cout << "Computer played: ";
        display_move(comp);

        cout << "Result: ";
        res = game_func(p1, comp);
        switch (res)
        {
        case 0:
            cout << "draw" << endl;
            break;
        case 1:
            cout << "player wins" << endl;
            player++;
            break;
        case -1:
            cout << "computer wins" << endl;
            computer++;
            break;
        }
        cout << "--------------------------\n"<<endl;
    }
}


//This function uses the calculated scores and proceeds to declare the winner and prompts another match if the game ends in a draw
void results()
{   
    if(player == computer)
    {
        cout << "Draw \nPlus one match\n";
        cout << "-+-+-+-+-+-+-+-+-+-+-+-+-+\n"<<endl;
        rounds = 1;
        game_play();

        results();
    }
    else
    {
        if(player > computer) cout << "Player wins" << endl;
        else if(player < computer) cout << "Computer wins" << endl;
        cout << "Score: " << player << "-" << computer;
    }

    cout << "The End" << endl;
    cout << "##########################\n" << endl;
}


//This is the main function
int main()
{
    //Game name and initializaton
    game_intro();

    //Taking moves, calculating result, updating scores
    game_play();

    //display_moveing results along with scores
    results();
}
