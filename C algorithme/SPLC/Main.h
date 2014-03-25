//SPLC analyses
//For USE Patents&Standards course
//By Frank Boerman Tue 2014(c)
//Main headerfile

#ifndef MAIN_H
#define MAIN_H

#include "rapidjson\document.h"
#include <string>
#include "List.h"

//globals
rapidjson::Document Edges;
rapidjson::Document Nodes;
List<int>* BeginPoints;
List<int>* EndPoints;

//functions

//main function
int main(int argc, char* argv[]);
//reads the json from file and stores it in given object
void ReadJson(rapidjson::Document* document, std::string fname);
//walk to next point
void WalkNext(int parent, int child, List<std::string> visitededges, List<int> visitednodes, int* iterations);
//starts the SPCL algorithm
void SPLC();
//creates an integer list from json
List<int>* makeList(rapidjson::Document* d);
//returns current time
std::string GetTime();
#endif