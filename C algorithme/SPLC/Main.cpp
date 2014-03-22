//SPLC analyses
//For USE Patents&Standards course
//By Frank Boerman Tue 2014(c)
//Main sourcefile

#include <string>
#include <iostream>
#include <fstream>
#include "rapidjson\document.h"
#include "Main.h"
#include "List.h"
#include <sstream>

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

List<int> makeList(Document* d)
{
	List<int>* lijstje = new List<int>();
	const Value& jsonlijst = *d;
	for (SizeType i = 0; i < d->Size(); i++)
	{
		lijstje->append(jsonlijst[i].GetInt());
	}
	return *lijstje;
}

void WalkNext(int parent, int child, List<std::string> visitededges, List<int> visitednodes, int* iterations)
{
	(*iterations)++;
	std::stringstream edge;
	edge << parent << "." << child;
	visitededges.append(edge.str());
	visitednodes.append(child);
	if (EndPoints.Search(child))
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
			std::string c = nodes_child[i].GetString();
			edge.str(" ");
			edge.clear();
			edge << child << "." << c;
			if (visitededges.Search(edge.str()) || visitednodes.Search(atoi(c.c_str())))
			{
				continue;
			}
			else
			{
				WalkNext(child, atoi(c.c_str()), visitededges, visitednodes,iterations);
			}
		}
	}
}

void SPLC()
{
	for (int i = 0; i < BeginPoints.len(); i++)
	{
		int BP = BeginPoints.Get_Int(i);
		const Value& BP_nodes = Nodes[std::to_string(BP).c_str()];
		for (int j = 0; j < BP_nodes.Size(); j++)
		{
			int iterations = 0;
			int child = BP_nodes[i].GetInt();
			std::cout << "Begin with edge " << BP << "." << child << std::endl;
			List<std::string>* visitededges = new List<std::string>();
			List<int>* visitednodes = new List<int>();
			WalkNext(BP, child, *visitededges, *visitednodes, &iterations);
			std::cout << "Finished in " << iterations << std::endl;
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

	//int test_check = EndPoints.HasMember("9");
	//List<std::string>* lijstje = new List<std::string>("testitem");
	//lijstje->append("yolo");
	//std::string test = lijstje->Get_String(1);

	//List<int>* lijstje2 = new List<int>(1);
	//lijstje2->append(5);
	//int testint = lijstje2->Get_Int(1);
	//lijstje2->pop();
	//int testint2 = lijstje2->Get_Int(1);
	//bool search = lijstje->Search("yolo");
	//bool search2 = lijstje2->Search(1);
	//int test = Nodes["21"]["19"].GetInt();
	//Type test = EndPoints.GetType();
	//const Value& list = EndPoints;
	//SizeType i = 0;
	//int testint = list[i].GetInt();
	return 0;
	
}