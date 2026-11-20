#pragma once
#include <cstddef>
#include <cerrno>
#include <cstdlib>
#include <cmath>
#include <climits>
namespace lord_sumi {
enum Type{Text,Integer,Number,Boolean};
struct Rule{Type type;bool required;};
enum Status{Valid,Missing,Invalid,Fault};
template<size_t MAX_FIELDS> class Contract {
 Rule rules_[MAX_FIELDS];size_t count_=0;bool fault_=false;
 static bool empty(const char*s){return !s||!*s;}
 static bool parse(const char*s,Type t){
  if(t==Text)return true;
  if(t==Boolean)return (s[0]=='0'&&!s[1])||(s[0]=='1'&&!s[1])||(s[0]=='t'&&s[1]=='r'&&s[2]=='u'&&s[3]=='e'&&!s[4])||(s[0]=='f'&&s[1]=='a'&&s[2]=='l'&&s[3]=='s'&&s[4]=='e'&&!s[5]);
  if(*s==' '||*s=='\t'||*s=='\n')return false;
  char*end=nullptr;errno=0;
  if(t==Integer){long n=strtol(s,&end,10);(void)n;return errno!=ERANGE&&end!=s&&!*end;}
  double n=strtod(s,&end);return errno!=ERANGE&&end!=s&&!*end&&std::isfinite(n);
 }
public:
 bool add(Rule r){if(fault_)return false;if(count_==MAX_FIELDS||r.type<Text||r.type>Boolean){fault_=true;return false;}rules_[count_++]=r;return true;}
 Status check(size_t index,const char*value)const{if(fault_||index>=count_)return Fault;if(empty(value))return rules_[index].required?Missing:Valid;return parse(value,rules_[index].type)?Valid:Invalid;}
 void reset(){count_=0;fault_=false;}bool fault()const{return fault_;}
};
}