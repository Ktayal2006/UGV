#include <iostream>
#include <vector>
#include <string>
#include <utility>

using namespace std;

enum Move {
    COOPERATE,
    DEFECT
};

// A strategy is a function that takes the opponent's history and returns a move.
using Strategy = Move (*)(const vector<Move>&);

std::pair<int, int> payoff_matrix[2][2] = {
    { {3, 3}, {0, 5} }, 
    { {5, 0}, {1, 1} } 
};

pair<int, int> play_round(Strategy strategy_a, Strategy strategy_b, 
                               const vector<Move>& history_a, const vector<Move>& history_b) {
    Move move_a = strategy_a(history_b); // A's strategy considers B's history
    Move move_b = strategy_b(history_a); // B's strategy considers A's history

    // Convert moves to indices for the payoff matrix.
    int a_idx = (move_a == COOPERATE) ? 0 : 1;
    int b_idx = (move_b == COOPERATE) ? 0 : 1;

    return payoff_matrix[a_idx][b_idx];
}

// --- Strategy Implementations ---
Move always_defect(const std::vector<Move>& history) {
    return DEFECT;
}

Move tit_for_tat(const std::vector<Move>& history) {
    if (history.empty()) {
        return COOPERATE;
    }
    return history.back();
}

Move forgiving_tit_for_tat(const std::vector<Move>& history) {
    if (history.empty()) {
        return COOPERATE;
    }

    if (history.back() == COOPERATE) {
        return COOPERATE;
    }

    if (rand() % 10 == 0) {
        return COOPERATE; 
    } else {
        return DEFECT; 
    }
}

// --- Tournament Simulation ---
void run_tournament(int N, Strategy strategy_a, Strategy strategy_b,
                    const string& strategy_name_a, const string& strategy_name_b) {
    vector<Move> history_a;
    vector<Move> history_b;
    int score_a = 0;
    int score_b = 0;

    for (int i = 0; i < N; ++i) {
        pair<int, int> round_scores = play_round(strategy_a, strategy_b, history_a, history_b);
        score_a += round_scores.first;
        score_b += round_scores.second;

        history_a.push_back(strategy_a(history_b));
        history_b.push_back(strategy_b(history_a));
    }

    cout << "Matchup: " << strategy_name_a << " vs. " << strategy_name_b << std::endl;
    cout << "Final Scores (after " << N << " rounds):" << std::endl;
    cout << "  " << strategy_name_a << " Score: " << score_a << " points" << std::endl;
    cout << "  " << strategy_name_b << " Score: " << score_b << " points" << std::endl;
    cout << "----------------------------------------" << std::endl;
}

int main() {
    const int N = 5; // Number of rounds

    std::cout << "--- Game Simulation Results (N = " << N << " rounds) ---" << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    
    // Match 1: tit_for_tat vs. always_defect
    run_tournament(N, tit_for_tat, always_defect, "Tit-for-Tat", "Always-Defect");

    // Match 2: tit_for_tat vs. forgiving_tit_for_tat
    run_tournament(N, tit_for_tat, forgiving_tit_for_tat, "Tit-for-Tat", "Forgiving-Tit-for-Tat");

    // Match 3: always_defect vs. forgiving_tit_for_tat
    run_tournament(N, always_defect, forgiving_tit_for_tat, "Always-Defect", "Forgiving-Tit-for-Tat");

    return 0;
}
