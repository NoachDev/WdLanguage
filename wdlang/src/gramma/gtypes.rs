use serde_yaml;
use std::{path::PathBuf, collections::HashMap};
use crate::lexer;

use super::{scopes, ROOT_WD, SEP_WD};
use lazy_static::lazy_static;

lazy_static!{
  pub static ref ELEMENTS_FIELDS : HashMap<String, HashMap<String, Vec<String>>> = serde_yaml::from_str(include_str!("elements.yml")).expect("error on load elements");
}

#[derive(Debug, PartialEq)]
pub struct Widget{
  pub name      : String,
  pub element_type  : Option<String>,

  pub presets   : Box<[String]>,
  
  pub atributs  : scopes::WdDatas,
  pub commands  : scopes::WdDatas,

  pub others    : scopes::WdDatas,

  pub comments  : String
}

#[derive(Debug)]
pub struct WdVars{
  pub __master__ : String,
  pub others : scopes::WdDatas
}

#[derive(Debug)]
pub struct Preset{
  pub name : String,
  pub others  : scopes::WdDatas
}

#[derive(Debug)]
pub struct Method{
  pub name : String,
  pub parameters : Box<[String]>,

  pub calls : scopes::WdDatas,
  pub widget : Widget

}

#[derive(Debug)]
pub struct WdTemplate{
  pub name    : String,

  pub widgets : Vec<Widget>,
  pub wd_vars : WdVars,
  pub presets : Vec<Preset>,
  pub methods : Vec<Method>,

  pub script  : Option<PathBuf>
}

impl WdTemplate {

  fn element_widget(&self, scopes : & mut scopes::BoxScopes) -> Widget{
    let fields_widget = ELEMENTS_FIELDS.get("widgets").unwrap();

    let name  = scopes.find_key(fields_widget.get("name").unwrap()).expect("wdigets need one name (id)").value.args.unwrap().first().unwrap().trim().to_lowercase();

    let presets : Box<[String]> = {  
      if let Ok(prs) = scopes.find_key(fields_widget.get("presets").unwrap()){
        prs.value.args.unwrap()
      }
      else{
        Box::new([])
      }
    };

    let elm_type : Option<String> = {
      if let Ok(elm_t) = scopes.find_key(fields_widget.get("elm_type").unwrap()){
        Some(elm_t.value.args.unwrap().first().unwrap().to_string())
      }
      else{
        None
      }
    };

    Widget {
      name: name,
      element_type : elm_type,
      presets: presets,
      atributs: scopes.get_segments(lexer::ltypes::TypesObject::Segments(lexer::ltypes::TypesSegment::Atributs)),
      commands: scopes.get_segments(lexer::ltypes::TypesObject::Segments(lexer::ltypes::TypesSegment::Commands)),
      others : scopes.main_scope.as_mut().unwrap().1.drain(0..).collect(),
      comments : scopes.comments.drain(0..).collect()
    }
  }

  pub fn create_element_widget(& mut self, scopes : & mut scopes::BoxScopes){
    self.widgets.push(
      self.element_widget(scopes)
    )

  }

  pub fn create_element_wdvars(& mut self, scopes : & mut scopes::BoxScopes){
    self.wd_vars.others.append(& mut scopes.main_scope.as_mut().unwrap().1)
  }

  pub fn create_element_preset(& mut self, scopes : & mut scopes::BoxScopes){
    
    self.presets.push(
      Preset{
        name : scopes.find_key(ELEMENTS_FIELDS.get("presets").unwrap().get("name").unwrap()).expect("presets need one name (id)").value.args.unwrap().first().unwrap().to_string(),
        others : scopes.main_scope.as_mut().unwrap().1.drain(0..).collect()
      }
    )
  }

  pub fn create_element_method(& mut self, scopes : & mut scopes::BoxScopes){
    let mathod_fields = ELEMENTS_FIELDS.get("methods").unwrap();

    let name  = scopes.find_key(mathod_fields.get("name").unwrap()).expect("methods need one name (id)").value.args.unwrap().first().unwrap().trim().to_string();
    let parm  = {
      if let Ok(field) = scopes.find_key(mathod_fields.get("parmeters").unwrap()){
        field.value.args.unwrap()
      }
      else{
        Box::new([])
      }
    };

    scopes.main_scope.as_mut().unwrap().1.push(
      lexer::ltypes::LineData {
        line: 0,
        kind: lexer::ltypes::TypesLineData::Local,
        key: ELEMENTS_FIELDS.get("widgets").unwrap().get("name").unwrap().last().unwrap().to_string(),
        value: lexer::ltypes::DataValue { args: Some(Box::new([name.clone()])), kwargs: None }
      }
    );

    self.methods.push(
      Method{
        name : name.clone(),
        parameters : parm,
        calls : scopes::WdDatas::new(),
        widget : self.element_widget(scopes)
        
      }
    )
  }

  pub fn call_method(& mut self, data : lexer::ltypes::LineData ){
    for i in self.methods.iter_mut(){
      if i.name == data.key.trim(){
        i.calls.push(data);
        break;
      }
    }
  }
  pub fn new(file : &PathBuf, base_fnc : & PathBuf, master : &String) -> Self{

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

    name =  master.to_string() + &name;

    if name.len() == 0{
      name = ROOT_WD.to_string();
    }

    Self{
      name    : name.clone(),
      widgets : Vec::new(),
      wd_vars : WdVars { __master__: name, others: Vec::new() }, // add name
      presets : Vec::new(),
      methods : Vec::new(),
      script  : script
    
    }
  }

}
