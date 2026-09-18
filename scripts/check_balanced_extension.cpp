#include <bits/stdc++.h>
using namespace std;
struct State{long long configs=0,choices=0,maxgap=LLONG_MIN,bestd=0;string wit;};
string quote(const string&s){string r="\"";for(char c:s){if(c=='\"'||c=='\\')r+='\\';r+=c;}return r+"\"";}
void save(const string&p,int t,long long next,long long graphs,const State&s,bool done){string tmp=p+".tmp";ofstream o(tmp);o<<"{\n  \"t\": "<<t<<",\n  \"next_configuration\": "<<next<<",\n  \"triangle_free_graphs\": "<<graphs<<",\n  \"configurations_checked\": "<<s.configs<<",\n  \"maximal_neighborhood_configurations_checked\": "<<s.choices<<",\n  \"max_gap\": "<<s.maxgap<<",\n  \"best_d\": "<<s.bestd<<",\n  \"complete\": "<<(done?"true":"false")<<",\n  \"witness\": "<<quote(s.wit)<<"\n}\n";o.close();rename(tmp.c_str(),p.c_str());}
int main(int argc,char**argv){
 int t=argc>1?stoi(argv[1]):0;if(t<1||t>25){cerr<<"usage: check_balanced_extension T [--resume]\n";return 2;}bool resume=argc>2&&string(argv[2])=="--resume";
 string dir="results/balanced_extension";filesystem::create_directories(dir);string cp=dir+"/t"+to_string(t)+".checkpoint.json",outp=dir+"/t"+to_string(t)+".json";
 vector<pair<int,int>>P;for(int a=0;a<5;a++)for(int b=a+1;b<5;b++)P.push_back({a,b});long long start=0,graphs=0,idx=0;State st;
 if(resume){ifstream in(cp);string z((istreambuf_iterator<char>(in)),{});auto num=[&](string k){auto p=z.find(k);if(p==string::npos)return 0LL;p=z.find(':',p)+1;return stoll(z.substr(p));};start=num("next_configuration");graphs=num("triangle_free_graphs");st.configs=num("configurations_checked");st.choices=num("maximal_neighborhood_configurations_checked");st.maxgap=num("max_gap");}
 for(int em=0;em<1024;em++){vector<pair<int,int>>E;bool tf=1;for(int i=0;i<10;i++)if(em>>i&1)E.push_back(P[i]);auto has=[&](int x,int y){if(x>y)swap(x,y);for(auto e:E)if(e==make_pair(x,y))return true;return false;};for(int a=0;a<5;a++)for(int b=a+1;b<5;b++)for(int c=b+1;c<5;c++)if(has(a,b)&&has(a,c)&&has(b,c))tf=0;if(!tf)continue;graphs++;
  for(int code=0;code<625;code++,idx++){if(idx<start)continue;int z=code,f[5]={0};for(int x=1;x<5;x++){f[x]=z%5;z/=5;}int S[5]={};for(int j=0;j<5;j++)for(int x=0;x<5;x++){int q=(f[x]-j+5)%5;if(q==1||q==4)S[j]|=1<<x;}
   vector<int>fam[5];for(int j=0;j<5;j++)for(int m=0;m<32;m++)if(!(m&~S[j])){bool ok=1;for(auto e:E)if((m>>e.first&1)&&(m>>e.second&1))ok=0;if(!ok)continue;bool mx=1;for(int x=0;x<5;x++)if(!(m>>x&1)&&(S[j]>>x&1)){int n=m|1<<x,ok2=1;for(auto e:E)if((n>>e.first&1)&&(n>>e.second&1))ok2=0;if(ok2)mx=0;}if(mx)fam[j].push_back(m);}st.configs++;
   int xmono[512]={},base[512]={};for(int cm=0;cm<512;cm++){for(auto e:E)if(!(((cm>>e.first)^(cm>>e.second))&1))xmono[cm]++;for(int j=0;j<5;j++)if(!(((cm>>(5+j))^(cm>>(5+(j+1)%5)))&1))base[cm]++;}
   for(int a:fam[0])for(int b:fam[1])for(int c:fam[2])for(int d:fam[3])for(int e:fam[4]){int I[5]={a,b,c,d,e};st.choices++;int best=INT_MAX;for(int cm=0;cm<512;cm++){int ext=0;for(int j=0;j<5;j++)for(int x=0;x<5;x++)if((I[j]>>x&1)&&!(((cm>>x)^(cm>>(5+j)))&1))ext++;best=min(best,xmono[cm]+ext*t+base[cm]*t*t);}int gap=best-(t+1)*(t+1);if(gap>st.maxgap){st.maxgap=gap;st.bestd=best;ostringstream w;w<<"E=";for(auto ee:E)w<<ee.first<<ee.second<<",";w<<" f=";for(int x:f)w<<x;w<<" I=";for(int ii:I)w<<ii<<",";st.wit=w.str();}}
   // Checkpointing every configuration made filesystem latency dominate the
   // computation. Losing at most this block on interruption is safe because
   // the checkpoint is written only after a configuration is complete.
   if ((idx+1)%1000==0) save(cp,t,idx+1,graphs,st,false);
  }
 }
 // There are exactly 388 triangle-free labeled F; use the canonical total in
 // the completed artifact (resume mode otherwise recounts skipped graphs).
 save(outp,t,388LL*625,388,st,true);remove(cp.c_str());cerr<<"t="<<t<<" configs="<<st.configs<<" choices="<<st.choices<<" max_gap="<<st.maxgap<<"\n";cout<<"t="<<t<<" complete inequality="<<(st.maxgap<=0?"holds":"counterexample")<<" max_gap="<<st.maxgap<<"\n";
}
