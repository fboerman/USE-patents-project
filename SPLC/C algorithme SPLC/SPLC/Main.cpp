//SPLC analyses
//For USE Patents&Standards course
//By Frank Boerman Tue 2014(c)
//Main sourcefile

//the libraries
#include <string>
#include <iostream>
#include <fstream>
#include "rapidjson/document.h"
#include "rapidjson/filestream.h"
#include "rapidjson/prettywriter.h"
#include "Main.h"
#include "List.h"
#include <sstream>
#include <cstdio>
#include <stdio.h>
#include <ctime>


using namespace rapidjson;

void ReadJson(Document* d, std::string fname) //read the given json file and parse it to an json Document object
{
	std::ifstream file;
	std::string line;

	file.open(fname);
	if (file.fail())
	{
		std::cout << "Error reading file " << fname << std::endl;
		return;
	}
	//get line from file (always one line so no loop)
	getline(file, line);
	d->Parse<0>(line.c_str());
	file.close();
}

List<int>* makeList(Document* d) //copy an json array object to a integer list
{
	List<int>* lijstje = new List<int>();
	const Value& jsonlijst = *d;
	for (SizeType i = 0; i < d->Size(); i++)
	{
		lijstje->append(jsonlijst[i].GetInt());
	}
	return lijstje;
}

void WalkNext(int parent, int child, List<std::string>* visitededges, List<int>* visitednodes, int* iterations) //recursive routine that visits all nodes
{
	(*iterations)++; //update counter
	std::stringstream edge;
	edge << parent << "." << child; //create edgename
	visitededges->append(edge.str()); //update visited node and edge
	visitednodes->append(child);
	if (EndPoints->Search(child)) //check if endpoint is reached
	{
		for (int i = 0; i < visitededges->len(); i++) //if so, loop over all visited edges
		{
			Edges[visitededges->Get_String(i).c_str()].SetInt(Edges[visitededges->Get_String(i).c_str()].GetInt() + 1); //and count +1 to the value of that edge
		}
		//delete this point and edge from the visited list, because path has ended
		visitededges->pop();
		visitednodes->pop();
		return; //endpoint reached so go one up
	}
	else//if not
	{
		const Value& nodes_child = Nodes[std::to_string(child).c_str()]; //convert children of child(aka current node were sitting on) to a handy list
		for (SizeType i = 0; i < nodes_child.Size(); i++) //loop through said list
		{
			int c = nodes_child[i].GetInt(); //fetch selected node
			edge.str(" ");
			edge.clear();
			edge << child << "." << c; //create edgename (after clearing stringstream buffer)
			if (visitededges->Search(edge.str()) || visitednodes->Search(c))
			{
				//if this node or edge is already visited in the past, skip it (loop detection, otherwise we get stuck in an infinite loop)
				continue;
			}
			else
			{
				WalkNext(child, c, visitededges, visitednodes,iterations); //if not that visit the selected node
			}
		}
	}
	//delete this point and edge from the visited list, because this is deadend path (if execution reaches this
	visitededges->pop();
	visitednodes->pop();
}

void SPLC() //the main SPLC algorithm
{
	int iterationstotal = 0; //counter for total interations
	for (int i = 0; i < BeginPoints->len(); i++) //loops over the beginpoints list
	{
		int BP = BeginPoints->Get_Int(i);//fetches the selected point
		const Value& BP_nodes = Nodes[std::to_string(BP).c_str()]; //converts the json entry of this point to a handy list
		for (SizeType j = 0; j < BP_nodes.Size(); j++)//loops over the json entry of the selected beginpoint, aka loops over the children
		{
			int iterations = 0; //counter for iterations for this child of beginpoint
			int child = BP_nodes[j].GetInt(); //fetches the selected child
			//std::cout << "Begin with edge " << BP << "." << child << " at " << GetTime() <<std::endl; //notification with time and subject
			std::cout << BP << "." << child << "\t\t\t" << GetTime() << std::endl;
			List<std::string>* visitededges = new List<std::string>(); //create an empty list of strings for the edges
			List<int>* visitednodes = new List<int>(BP); //create an empty list of integers for the nodes, with the beginpoint set as already visited
			WalkNext(BP, child, visitededges, visitednodes, &iterations); //start the recursive routine that walks over the points
			//free the memory
			delete visitededges;
			delete visitednodes;
			//std::cout << "Finished in " << iterations << " iterations at " << GetTime() << std::endl;//notification with time, subject and number of iterations
			std::cout << BP << "." << child << "\t" << iterations << "\t\t" << GetTime() << std::endl;
			iterationstotal += iterations;
		}
	}
	std::cout << "Done running at " << GetTime() << " after " << iterationstotal << " iterations" << std::endl;
}

std::string GetTime()
{
	std::stringstream stream;
	time_t tijd = time(0);
	struct tm * now = localtime(&tijd);
	stream << now->tm_hour << ":" << now->tm_min << ":" << now->tm_sec;
	return stream.str();
}

int main(int argc, char* argv[])
{
	//read the json files and store them in the correct globals
	ReadJson(&Edges, "json/edges.json");
	ReadJson(&Nodes, "json/nodes.json");
	Document json;
	ReadJson(&json, "json/beginpoints.json");
	BeginPoints = makeList(&json);
	ReadJson(&json, "json/endpoints.json");
	EndPoints = makeList(&json);
	
	//activate the algorithm
	SPLC();
	//open the filestream
	FILE* stream = fopen("json/outputedges.json","w");
	//save the document
	FileStream f(stream);
	Writer<FileStream> writer(f);
	Edges.Accept(writer);
	//flush stream to disk
	fclose(stream);
	std::cin.ignore();
	return 0;
	
}