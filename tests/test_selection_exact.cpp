// Standalone regression tests, using the very predicates used by the auditor.
#define main audit_program_main
#include "../scripts/audit_selection_exact.cpp"
#undef main
array<int,10> adjacency(vector<E> es){array<int,10>a{};for(auto [u,v]:es){a[u]|=1<<v;a[v]|=1<<u;}return a;}
bool reference_shape(int s,const array<int,10>& a){
 bool independent=true;for(int u=0;u<10;u++)if(s>>u&1)independent &= !(a[u]&s);
 if(independent)return true;
 // Independent definition: enumerate every nonempty two-sided partition.
 for(int p=(s-1)&s;p;p=(p-1)&s){int q=s^p;if(!q)continue;bool ok=true;
  for(int u=0;u<10;u++)if(s>>u&1)for(int v=u+1;v<10;v++)if(s>>v&1)
   if(bool(a[u]>>v&1)!=bool((p>>u&1)!=(p>>v&1)))ok=false;
  if(ok)return true;
 }return false;
}
int main(){
 auto p4=adjacency({{0,1},{1,2},{2,3}});assert(!shape(15,p4));
 assert(!shape(15,adjacency({{0,1},{2,3}}))); // 2K2
 assert(!shape(7,adjacency({{0,1}}))); // edge plus isolate
 assert(!shape(7,adjacency({{0,1},{1,2},{0,2}})));
 assert(shape(31,adjacency({{0,2},{0,3},{0,4},{1,2},{1,3},{1,4}})));
 assert(shape(1023,adjacency({})));assert(shape(0,p4));
 assert(allowed_flip(15,p4)); // legal via its independent complement
 auto two_paths=adjacency({{0,1},{1,2},{2,3},{4,5},{5,6},{6,7}});
 assert(!allowed_flip(15,two_paths)); // neither side is an allowed shape
 // Exhaustive predicate comparison for all labeled graphs on five vertices.
 vector<E>pairs;for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)pairs.emplace_back(i,j);
 for(int g=0;g<1024;g++){vector<E>es;for(int b=0;b<10;b++)if(g>>b&1)es.push_back(pairs[b]);auto a=adjacency(es);
  for(int s=0;s<32;s++)assert(shape(s,a)==reference_shape(s,a));
 }
 // Larger numerator need not mean larger rational value, for either sign.
 assert(greater_fraction(2,2,8,10));assert(!greater_fraction(8,10,2,2));
 assert(greater_fraction(-8,10,-2,2));assert(!greater_fraction(-2,2,-8,10));
 assert(!greater_fraction(1,2,2,4));assert(!greater_fraction(2,4,1,2));
 cout<<"PASS: shape regressions, 32768 exhaustive predicate checks, rational comparisons\n";
}
