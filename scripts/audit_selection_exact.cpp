#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using E=pair<int,int>;
int mono(const vector<E>& es,int s){int r=0;for(auto [u,v]:es)r+=((s>>u&1)==(s>>v&1));return r;}
// An edge-containing complete bipartite induced graph has no isolated vertices.
bool shape(int s,const array<int,10>& adj){
 int u=-1;for(int v=0;v<10;v++)if((s>>v&1)&&(adj[v]&s)){u=v;break;}
 if(u<0)return true;
 int Q=adj[u]&s,P=s^Q;
 for(int v=0;v<10;v++)if(s>>v&1)if((adj[v]&s)!=((P>>v&1)?Q:P))return false;
 return true;
}
bool allowed_flip(int s,const array<int,10>& adj){return shape(s,adj)||shape(s^1023,adj);}
bool greater_fraction(long long an,long long ad,long long bn,long long bd){
 assert(ad>0&&bd>0);return an*bd>bn*ad;
}
int main(){
 string name,g6;int n,m,expected;
 while(cin>>name>>g6>>n>>m>>expected){
  assert(n==15);vector<E> es(m);for(auto& [u,v]:es)cin>>u>>v;
  int dg=1000;for(int s=0;s<32768;s+=2)dg=min(dg,mono(es,s));assert(dg==expected);
  int count=0,bestnum=-100000,bestden=1;
  for(int i=0;i<11;i++)for(int j=i+1;j<12;j++)for(int l=j+1;l<13;l++)for(int p=l+1;p<14;p++)for(int r=p+1;r<15;r++){
   array<int,5>X={i,j,l,p,r};int idx[15],h=0;fill(idx,idx+15,-1);for(int t=0;t<5;t++)idx[X[t]]=10+t;for(int v=0;v<15;v++)if(idx[v]<0)idx[v]=h++;
   vector<E> he,xe,be;array<int,10>adj{};
   for(auto [u,v]:es){u=idx[u];v=idx[v];if(u<10&&v<10){he.emplace_back(u,v);adj[u]|=1<<v;adj[v]|=1<<u;}else if(u>=10&&v>=10)xe.emplace_back(u-10,v-10);else{if(u>=10)swap(u,v);be.emplace_back(u,v-10);}}
   int hm[1024],xm[32],dh=1000,dx=1000;vector<int>cs,as,allowed;
   for(int s=0;s<1024;s++){hm[s]=mono(he,s);dh=min(dh,hm[s]);}
   for(int a=0;a<32;a++){xm[a]=mono(xe,a);dx=min(dx,xm[a]);}
   for(int c=0;c<1024;c+=2)if(hm[c]==dh)cs.push_back(c);
   for(int a=0;a<32;a++)if(xm[a]==dx)as.push_back(a);
   for(int s=0;s<1024;s++)if(allowed_flip(s,adj))allowed.push_back(s);
   assert(!allowed.empty()&&allowed.front()==0&&allowed.back()==1023);
   int cost[32][1024];for(int a:as)for(int c=0;c<1024;c++){int z=0;for(auto [u,v]:be)z+=((c>>u&1)==(a>>v&1));cost[a][c]=dx+z+hm[c]-dh;}
   int best=100000,bc=-1;for(int c:cs){int sum=0;for(int a:as){int low=1000;for(int s:allowed)low=min(low,cost[a][c^s]);sum+=low;}if(sum<best){best=sum;bc=c;}}
   int den=as.size(),num=5*den-best;assert(den>0&&bc>=0&&best>=(dg-dh)*den);
   if(greater_fraction(num,den,bestnum,bestden)){bestnum=num;bestden=den;}
   // Tab-separated fields; graph6 stays in the driver's JSON manifest.
   cout<<name<<'\t'<<i<<','<<j<<','<<l<<','<<p<<','<<r<<'\t'<<num<<'\t'<<den<<'\t'<<dg<<'\t'<<dh<<'\t'<<dx<<'\t'<<be.size()<<'\t'<<bc<<'\t'<<allowed.size()<<'\n';count++;
  }
  cout.flush();assert(count==3003);cerr<<name<<" complete, max margin "<<bestnum<<'/'<<bestden<<'\n';if(bestnum<0)break;
 }
}
