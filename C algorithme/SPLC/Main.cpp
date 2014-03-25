//SPLC analyses
//For USE Patents&Standards course
//By Frank Boerman Tue 2014(c)
//Main sourcefile

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


using namespace rapidjson;

void ReadJson(Document* d, std::string fname)
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

List<int>* makeList(Document* d)
{
	List<int>* lijstje = new List<int>();
	const Value& jsonlijst = *d;
	for (SizeType i = 0; i < d->Size(); i++)
	{
		lijstje->append(jsonlijst[i].GetInt());
	}
	return lijstje;
}

void WalkNext(int parent, int child, List<std::string> visitededges, List<int> visitednodes, int* iterations)
{
	(*iterations)++;
	std::stringstream edge;
	edge << parent << "." << child;
	visitededges.append(edge.str());
	visitednodes.append(child);
	if (EndPoints->Search(child))
	{
		for (int i = 0; i < visitededges.len(); i++)
		{
			Edges[visitededges.Get_String(i).c_str()].SetInt(Edges[visitededges.Get_String(i).c_str()].GetInt() + 1);
		}
		return;
	}
	else
	{
		const Value& nodes_child = Nodes[std::to_string(child).c_str()];
		for (SizeType i = 0; i < nodes_child.Size(); i++)
		{
			int c = nodes_child[i].GetInt();
			edge.str(" ");
			edge.clear();
			edge << child << "." << c;
			if (visitededges.Search(edge.str()) || visitednodes.Search(c))
			{
				continue;
			}
			else
			{
				WalkNext(child, c, *visitededges.clone(), *visitednodes.clone(),iterations);
			}
		}
	}
}

void SPLC()
{
	int iterationstotal = 0;
	for (int i = 0; i < BeginPoints->len(); i++)
	{
		int BP = BeginPoints->Get_Int(i);
		const Value& BP_nodes = Nodes[std::to_string(BP).c_str()];
		for (SizeType j = 0; j < BP_nodes.Size(); j++)
		{
			int iterations = 0;
			int child = BP_nodes[j].GetInt();
			std::cout << "Begin with edge " << BP << "." << child << std::endl;
			List<std::string>* visitededges = new List<std::string>();
			List<int>* visitednodes = new List<int>();
			WalkNext(BP, child, *visitededges, *visitednodes, &iterations);
			std::cout << "Finished in " << iterations << " iterations" << std::endl;
			iterationstotal += iterations;
		}
	}
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

	return 0;
	
}