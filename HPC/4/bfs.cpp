#include<bits/stdc++.h>
#include "omp.h"

#define n_nodes 7

using namespace std;
list<int>q;
vector<int>weight(n_nodes,1000);
bool visited[n_nodes];

struct Comparator {
    // Compare 2 Edges objects using weight
    bool operator ()(const int &e1, const int &e2){
        return weight[e1]<weight[e2];
    }
};

void bfs(int adj_matrix[n_nodes][n_nodes])
{
		if(q.empty())
			return;
    q.sort(Comparator());
		
		//pop first element and display it
		int cur_node = q.front();
    q.pop_front();
		printf("%d, ", cur_node);
	
		//For every element in the row of the adjacency matrix
		#pragma omp parallel for shared(visited,q,weight)
		for(int i=0; i<n_nodes; i++)
		{
			//If an unvisited Edge exists
			if(adj_matrix[cur_node][i]>0 && visited[i]==false)
			{

				//Replace the weight if it is larger
        if(weight[i] > adj_matrix[cur_node][i]){
            weight[i] = adj_matrix[cur_node][i];
        }

				//Push the destination of the smallest edge onto the queue
				q.push_back(i);
				visited[i]=true;
			}
		}
	
	//Call the function recursively
	bfs(adj_matrix);
}

int main(){
	
	//Get the maximum number of threads
  int th = omp_get_max_threads();
  cout<<"Number of Threads = "<<th<<endl;

	//Set the Adjacency Matrix
	int adj_matrix[n_nodes][n_nodes] = {
							{0	,10  ,15  ,0  ,0  ,0  ,0},
							{10	,0	,25	,25	,0	,0	,0},
							{15	,25	,0	,0	,40	,0	,0},
							{0	,25	,0	,0	,20	,0	,0},
							{0	,0	,40	,20	,0	,5	,0},
							{0	,0	,0	,0	,5	,0	,20},
							{0	,0	,0	,0	,0	,20	,0}
							};
	
	for(int i=0; i<n_nodes; i++){
		visited[i] = false;
	}

	int start_node = 3;

	q.push_back(start_node);
    weight[start_node] = 0;
	visited[start_node] = true;
	
	bfs(adj_matrix);

	return 0;
}