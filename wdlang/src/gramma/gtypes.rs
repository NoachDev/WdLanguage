use pcre2::bytes::Match;
use pyo3::{pyclass};
use serde_yaml;
use std::{path::PathBuf, collections::HashMap};
use crate::lexer;
use super::{scopes, ROOT_WD, SEP_WD};
use lazy_static::lazy_static;

lazy_static!{
  pub static ref ELEMENTS_FIELDS : HashMap<String, HashMap<String, Vec<String>>> = serde_yaml::from_str(include_str!("elements.yml")).expect("error on load elements");
}

#[pyclass]
#[derive(Debug, PartialEq, Clone)]
pub struct Widget{
  #[pyo3(get)]
  pub name      : String,
  #[pyo3(get)]
  pub element_type  : Option<String>,
  
  #[pyo3(get)]
  pub presets   : Vec<Preset>,


  #[pyo3(get)]
  pub atributs  : scopes::WdDatas,
  #[pyo3(get)]
  pub commands  : scopes::WdDatas,

  #[pyo3(get)]
  pub others    : scopes::WdDatas,

  #[pyo3(get)]
  pub comments  : String
}

#[derive(Debug)]
pub struct WdVars{
  pub __master__ : String,
  pub others : HashMap<String, lexer::ltypes::DataValue>
}

#[pyclass]
#[derive(Debug, Clone, PartialEq)]
pub struct Preset{
  #[pyo3(get)]
  pub name : String,
  #[pyo3(get)]
  pub others  : scopes::WdDatas
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Method{
  #[pyo3(get)]
  pub name : String,
  #[pyo3(get)]
  pub parameters : Vec<String>,

  #[pyo3(get)]
  pub calls : scopes::WdDatas,
  #[pyo3(get)]
  pub widget : Widget

}

pub struct Repository<'a>{
  pub wd_vars : WdVars,
  pub presets : Vec<Preset>,

  pub parent  : Option<&'a Repository<'a>>
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct WdTemplate{
  #[pyo3(get)]
  pub name    : String,

  #[pyo3(get)]
  pub widgets : Vec<Widget>,
  #[pyo3(get)]
  pub methods : Vec<Method>,
  
  #[pyo3(get)]
  pub script  : Option<PathBuf>,

}

impl WdTemplate {

  fn element_widget(&self, scopes : & mut scopes::BoxScopes, repo : & mut Repository) -> Widget{
    let fields_widget = ELEMENTS_FIELDS.get("widgets").unwrap();

    let name  = scopes.find_key(fields_widget.get("name").unwrap()).expect("wdigets need one name (id)").args.unwrap().first().unwrap().content.trim().to_lowercase();

    let presets : Vec<String> = {  
      if let Ok(prs) = scopes.find_key(fields_widget.get("presets").unwrap()){
        prs.args_list()
      }
      else{
        Vec::new()
      }
    };

    let elm_type : Option<String> = {
      if let Ok(elm_t) = scopes.find_key(fields_widget.get("elm_type").unwrap()){
        Some(elm_t.args.unwrap().first().unwrap().content.to_string())
      }
      else{
        None
      }
    };

    Widget {
      name: name,
      presets : repo.load_presets(presets),
      element_type : elm_type,
      atributs: scopes.get_segments(lexer::ltypes::TypesObject::Segments(lexer::ltypes::TypesSegment::Atributs)),
      commands: scopes.get_segments(lexer::ltypes::TypesObject::Segments(lexer::ltypes::TypesSegment::Commands)),
      others : scopes.main_scope.as_mut().unwrap().1.drain().collect(),
      comments : scopes.comments.drain(0..).collect()
    }
  }

  pub fn create_element_widget(& mut self, scopes : & mut scopes::BoxScopes, repo : & mut Repository){
    self.widgets.push(
      self.element_widget(scopes, repo)
    )

  }

  pub fn create_element_method(& mut self, scopes : & mut scopes::BoxScopes, repo : & mut Repository){
    let mathod_fields = ELEMENTS_FIELDS.get("methods").unwrap();

    let name  = scopes.find_key(mathod_fields.get("name").unwrap()).expect("methods need one name (id)").args.unwrap().first().unwrap().content.trim().to_string();
    
    let parm : Vec<String>  = {
      if let Ok(field) = scopes.find_key(mathod_fields.get("parmeters").unwrap()){
        field.args_list()
      }
      else{
        Vec::new()
      }
    };

    scopes.main_scope.as_mut().unwrap().1.insert(
      ELEMENTS_FIELDS.get("widgets").unwrap().get("name").unwrap().last().unwrap().to_string(),
      lexer::ltypes::DataValue {
        args: Some(vec![lexer::ltypes::StringVar::new(name.clone())]),
        kwargs: None
      }
    );

    self.methods.push(
      Method{
        name : name.clone(),
        parameters : parm,
        calls : scopes::WdDatas::new(),
        widget : self.element_widget(scopes, repo)
        
      }
    )
  }

  pub fn call_method(& mut self, data : lexer::ltypes::LineData ){
    for i in self.methods.iter_mut(){
      if i.name == data.key.trim(){
        i.calls.insert(i.name.clone(), data.value);
        break;
      }
    }
  }
  
  pub fn new(file : &PathBuf, base_fnc : & PathBuf, name_master : &String) -> Self{

    fn script_find(path : &PathBuf, name : &String) -> Option<PathBuf>{
      let script = path.join(format!("{name}.py"));
  
      if script.exists(){
        return Some(script);
      }
  
      return None;
    }

    let mut name  : String          = file.file_stem().unwrap().to_ascii_lowercase().to_str().unwrap().to_string();
    let script    : Option<PathBuf> = script_find(base_fnc, &name);

    if name == "__init__"{
      name = String::new()
    }

    else{
      name = SEP_WD.to_owned() + &name;
    }

    name =  name_master.to_string() + &name;

    if name.len() == 0{
      name = ROOT_WD.to_string();
    }

    Self{
      name    : name.clone(),
      widgets : Vec::new(),
      methods : Vec::new(),
      script  : script,
    }

  }

}

impl<'a> Repository<'a>{
  fn get_vars(&self, list_val : Vec<Match>, arg : & mut lexer::ltypes::StringVar){
    let mut undf : Vec<Match> = Vec::new();

    for cap_match in list_val{
      let word = String::from_utf8_lossy(cap_match.as_bytes()).to_string();

      let mut name  = word.as_str();
      let mut key : Option<&str> = None;

      if let Some(index) = word.find("."){
        name = word.split_at(index).0;
        key = Some(word.split_at(index).1);
      }

      if let Some(data) = self.wd_vars.others.get(name){

        let to_change : String;

        if key.is_some(){
          if data.kwargs.is_some(){
            to_change = data.kwargs.as_ref().unwrap().get(key.unwrap()).unwrap().content.to_string();
          }
          else{
            panic!("Not have kwargs in {}", name)
          }
        }
        else{
          to_change = data.args.as_ref().unwrap().last().unwrap().content.to_string();
        }

        arg.append_vars(word, to_change, cap_match.start());
        
        
      }
      
      else{
        undf.push(cap_match)
      }
    }

    if undf.len() > 0 && self.parent.is_some(){
      self.parent.unwrap().get_vars(undf, arg)
    }



  }

  fn filter_vars(& self , arg : & mut lexer::ltypes::StringVar ){
    let text = arg.content.to_string();
    let vec_w : Vec<Match>= lexer::simbolys::WORD_IDF.captures_iter(text.as_bytes()).filter_map(|x| x.unwrap().name("word")).collect();

    self.get_vars(vec_w, arg);
    
    arg.load_vars();
  }

  pub fn load_presets(& self, list_presets : Vec<String>) -> Vec<Preset>{
    let mut ret : Vec<Preset> = Vec::new();
    let mut notf : Vec<String> = Vec::new();

    for n in list_presets{
      if let Ok(index) =  self.presets.binary_search_by(|preset| preset.name.cmp(&n) ){
        ret.push(self.presets.get(index).unwrap().clone());
      }
      else{
        notf.push(n);
      }
    }

    if notf.len() > 0 && self.parent.is_some(){
      ret.append(& mut self.parent.as_ref().unwrap().load_presets(notf))
    }

    return ret;
  }
  
  pub fn put_vars(& mut self, data : & mut lexer::ltypes::DataValue){
    if data.args.is_some(){
      for i in data.args.as_mut().unwrap(){
        self.filter_vars(i)
      }
    }
    
    if data.kwargs.is_some(){
      for i in data.kwargs.as_mut().unwrap().values_mut(){
        self.filter_vars(i)
      }

    }
  }

  pub fn create_element_preset(& mut self, scopes : & mut scopes::BoxScopes){
    self.presets.push(
      Preset{
        name : scopes.find_key(ELEMENTS_FIELDS.get("presets").unwrap().get("name").unwrap()).expect("presets need one name (id)").args.unwrap().first().unwrap().content.to_string(),
        others : scopes.main_scope.as_mut().unwrap().1.drain().collect()
      }
    )
  }

  pub fn create_var(& mut self, data : lexer::ltypes::LineData ){
    self.wd_vars.others.insert(data.key, data.value);
  }

  pub fn new(name : String, parent  : Option<&'a Repository>) -> Self{
    Self{
      wd_vars : WdVars { __master__: name, others: HashMap::new() },
      presets : Vec::new(),
      parent : parent
    }
  }
}