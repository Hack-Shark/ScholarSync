#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    // Array of file names to be merged
    string fileNames[] = {"a_1.csv", "a_2.csv", "b_1.csv", "b_2.csv", "c_1.csv", "c_2.csv", "d_1.csv", "e_1.csv", "e_2.csv", "f_1.csv", "g_1.csv", "h_1.csv", "i_1.csv", "i_2.csv", "j_1.csv", "j_2.csv", "j_3.csv", "j_4.csv", "k_1.csv", "l_1.csv", "m_1.csv", "m_2.csv", "n_1.csv", "o_1.csv", "p_1.csv", "p_2.csv", "q_1.csv", "r_1.csv", "s_1.csv", "t_1.csv", "u_1.csv", "v_1.csv", "w_1.csv", "z_1.csv"};
    
    // Output file to store the merged content
    ofstream outputFile("a_to_z_csvdata.csv");
    
    // Iterate over each file name
    for (const string& fileName : fileNames) {
        // Open each input file
        ifstream inputFile(fileName);
        
        if (inputFile) {
            // If the output file is not empty, start the content of each file on a new line
            if (outputFile.tellp() != 0) {
                outputFile << endl;
            }
            
            // Read the contents of the input file and write them to the output file
            outputFile << inputFile.rdbuf();
            
            // Close the input file
            inputFile.close();
        } else {
            cerr << "Failed to open file: " << fileName << endl;
        }
    }
    
    // Close the output file
    outputFile.close();
    
    cout << "Files merged successfully." << endl;
    
    return 0;
}
