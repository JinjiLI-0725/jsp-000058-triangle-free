// Exact implication audit of saved graphs. Positive certificates permit early exit.
#define main corrected_auditor_unused_main
#include "audit_selection_exact.cpp"
#undef main
#include <iomanip>
#include <numeric>
struct Answer {int num,den,c,dx,z;};
vector<array<int,5>> five_sets(){vector<array<int,5>> xs;
 for(int a=0;a<11;a++)for(int b=a+1;b<12;b++)for(int c=b+1;c<13;c++)for(int d=c+1;d<14;d++)for(int e=d+1;e<15;e++)xs.push_back({a,b,c,d,e});return xs;}
int main(){string name,g6;int n,m,expected;
 while(cin>>name>>g6>>n>>m>>expected){
  assert(n==15);vector<E> es(m);array<int,15> ga{};for(auto&[u,v]:es){cin>>u>>v;ga[u]|=1<<v;ga[v]|=1<<u;}
  for(auto[u,v]:es)assert(!(ga[u]&ga[v]));
  int gm[32768];gm[0]=m;int dg=m;
  for(int s=1;s<32768;s++){int v=__builtin_ctz((unsigned)s),t=s&(s-1);gm[s]=gm[t]+2*__builtin_popcount(ga[v]&t)-__builtin_popcount(ga[v]);dg=min(dg,gm[s]);}
  if(expected>=0)assert(dg==expected);
  auto xs=five_sets();
  // Low boundary size is a deterministic ordering, not a search for new graphs.
  stable_sort(xs.begin(),xs.end(),[&](auto x,auto y){auto score=[&](auto z){int mask=0,s=0;for(int v:z)mask|=1<<v;for(int v:z)s+=__builtin_popcount(ga[v]&(~mask));return s;};return score(x)<score(y);});
  int checked=0,minq=100,zero_count=0;bool positive=false;array<int,5>witness{};Answer answer{};int hist[16]={};
  for(auto X:xs){
   int idx[15],h=0;fill(idx,idx+15,-1);for(int i=0;i<5;i++)idx[X[i]]=10+i;for(int v=0;v<15;v++)if(idx[v]<0)idx[v]=h++;
   array<int,10> adj{},boundary{};array<int,5>xa{};int mh=0,mx=0,z=0;
   for(auto[u,v]:es){u=idx[u];v=idx[v];if(u<10&&v<10){adj[u]|=1<<v;adj[v]|=1<<u;mh++;}else if(u>=10&&v>=10){u-=10;v-=10;xa[u]|=1<<v;xa[v]|=1<<u;mx++;}else{if(u>=10)swap(u,v);boundary[u]|=1<<(v-10);z++;}}
   int hm[1024],dh=mh;hm[0]=mh;for(int s=1;s<1024;s++){int v=__builtin_ctz((unsigned)s),t=s&(s-1);hm[s]=hm[t]+2*__builtin_popcount(adj[v]&t)-__builtin_popcount(adj[v]);dh=min(dh,hm[s]);}
   int q=dg-dh;assert(q>=0&&q<16);minq=min(minq,q);hist[q]++;checked++;
   // U>=q rules out positive margin here. Once a zero is known, no further
   // exact Phi evaluation on q>=5 sets is needed to establish maximum zero.
   if(q>5 || (q==5&&zero_count))continue;
   int xm[32],dx=mx;xm[0]=mx;for(int a=1;a<32;a++){int v=__builtin_ctz((unsigned)a),t=a&(a-1);xm[a]=xm[t]+2*__builtin_popcount(xa[v]&t)-__builtin_popcount(xa[v]);dx=min(dx,xm[a]);}
   vector<int>as,allowed;for(int a=0;a<32;a++)if(xm[a]==dx)as.push_back(a);
   // Empty flip gives U<=dx+z/2 for every optimal base.
   if(2*dx+z<10){positive=true;witness=X;answer={10-2*dx-z,2,-1,dx,z};break;}
   for(int s=0;s<1024;s++)if(allowed_flip(s,adj))allowed.push_back(s);
   int costs[32][1024];for(int a:as){int bc=0,w[10];for(int v=0;v<10;v++){int d=__builtin_popcount(boundary[v]),ones=__builtin_popcount(boundary[v]&a);bc+=d-ones;w[v]=2*ones-d;}
    int ext[1024];ext[0]=bc;costs[a][0]=dx+bc+hm[0]-dh;
    for(int s=1;s<1024;s++){int v=__builtin_ctz((unsigned)s),t=s&(s-1);ext[s]=ext[t]+w[v];costs[a][s]=dx+ext[s]+hm[s]-dh;}}
   int best=100000,base=-1,den=as.size();
   for(int c=0;c<1024;c+=2)if(hm[c]==dh){int sum=0;for(int a:as){int low=1000;for(int s:allowed)low=min(low,costs[a][c^s]);assert(low>=q);sum+=low;}
    if(sum<best){best=sum;base=c;}
    if(best<5*den)break; // rigorous positive certificate, not a claimed exact max
   }
   int num=5*den-best;
   if(num>=0){witness=X;answer={num,den,base,dx,z};if(num>0){positive=true;break;}zero_count++;}
  }
  bool zero=!positive&&zero_count;bool failure=zero&&minq<5;
  string status=positive?"positive_certificate":failure?"counterexample":zero?"zero_and_tight":"strictly_negative_maximum";
  cout<<"{\"id\":"<<quoted(name)<<",\"graph6\":"<<quoted(g6)<<",\"dG\":"<<dg<<",\"status\":"<<quoted(status)<<",\"five_sets_checked\":"<<checked<<",\"min_q_checked\":"<<minq<<",\"margin_lower_num\":"<<answer.num<<",\"margin_lower_den\":"<<(answer.den?answer.den:1)<<",\"core_mask_local\":"<<answer.c<<",\"dX\":"<<answer.dx<<",\"z\":"<<answer.z<<",\"X\":[";
  for(int i=0;i<5;i++){if(i)cout<<',';cout<<witness[i];}cout<<"],\"q_histogram_checked\":{";bool first=true;for(int q=0;q<16;q++)if(hist[q]){if(!first)cout<<',';first=false;cout<<quoted(to_string(q))<<':'<<hist[q];}cout<<"}}"<<endl;
  if(!positive)assert(checked==3003);if(failure){cerr<<"FIRST COUNTEREXAMPLE "<<name<<' '<<g6<<endl;return 0;}
 }
}
