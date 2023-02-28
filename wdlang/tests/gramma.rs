use wdlang::gramma;
use std::path::Path;

struct WidgetExpc<'a>{
  name : &'a str,
  element : Option<&'a str>,
  presets : Vec<&'a str>,
  atributes : Vec<&'a str>,
  commands : Vec<&'a str>,
  others : Vec<&'a str>,
  comments : &'a str
}

#[test]
fn load_elements(){

  assert!(gramma::gtypes::ELEMENTS_FIELDS.contains_key("widgets"));
  assert!(gramma::gtypes::ELEMENTS_FIELDS.contains_key("presets"));
  assert!(gramma::gtypes::ELEMENTS_FIELDS.contains_key("methods"));

}

#[test]
fn gramma_output(){
  
  let pages  = Path::new("../App_test/Pages/__init__.wd").to_path_buf();
  let func = Path::new("../App_test/Functions/").to_path_buf();

  assert!(pages.exists());
  assert!(func.exists());

  let (ret, repo) = gramma::main(pages, &func, &".".to_string(), None);

  let wid_1 = WidgetExpc{
    name : "__master__",
    element : None,
    presets : vec![],
    atributes : vec![],
    commands : vec!["title", "rowconfigure", "columnconfigure"],
    others : vec![],
    comments : ""

  };
  let wid_2 = WidgetExpc{
    name : "f_test",
    element : Some("Button"),
    presets : vec!["slim"],
    atributes : vec!["highlightthickness", "width", "height"],
    commands : vec!["place"],
    others : vec![],
    comments : ""

  };

  for (wid, expc) in ret.widgets.iter().zip([wid_1, wid_2]){
    verify_wdigets(wid, expc);

  }
  // verify_wdigets(ret.widgets);
  verify_vars(repo.wd_vars);
  verify_presets(repo.presets);
  verify_methods(ret.methods);

  assert_eq!(Some(func.join("__init__.py")), ret.script);

}

fn contains_in(src: Vec<&String>, expec : &Vec<&str>){
  for i in src{
    assert!(expec.contains(&i.trim()))
  }
}

fn verify_wdigets(widget : &gramma::gtypes::Widget, expected : WidgetExpc){
  assert_eq!(widget.name, expected.name);

  if widget.element_type.is_some() && expected.element.is_some(){
    assert_eq!(expected.element.unwrap(), widget.element_type.as_ref().unwrap().trim());
  }
  else{
    assert_eq!(expected.element.is_none(), widget.element_type.is_none());
  }

  assert_eq!(expected.presets.len(), widget.presets.len(), "len of presets in widget is unexpected");
  assert_eq!(expected.atributes.len(), widget.atributs.len(), "len of atributes in widget is unexpected ");
  assert_eq!(expected.commands.len(), widget.commands.len(), "len of commands in widget is unexpected ");
  assert_eq!(expected.others.len(), widget.others.len(), "len of others in widget is unexpected ");

  for i in widget.presets.iter(){
    assert!(expected.presets.contains(&i.name.trim()));
  }

  contains_in(widget.atributs.keys().collect::<Vec<&String>>(), &expected.atributes);
  contains_in(widget.commands.keys().collect::<Vec<&String>>(), &expected.commands);
  contains_in(widget.others.keys().collect::<Vec<&String>>(), &expected.others);

  assert_eq!(expected.comments , widget.comments, "expected other comment ")

}

fn verify_vars(vars : gramma::gtypes::WdVars){

  let list_key_names = ["test01","test02","test03","test04","test05","df_bg","df_destac","df_desabl","df_fg","font_family","font_size","font",];

  assert_eq!(".", vars.__master__, "expected the master name is (root)");
  assert_eq!(list_key_names.len(), vars.others.len(), "epected the number of variables is 15");

  for exp in list_key_names{
    assert!(vars.others.contains_key(exp), "key of vars")
  }

}

fn verify_presets(presets : Vec<gramma::gtypes::Preset>){
  let first = &presets[0];
  
  assert_eq!(1, presets.len());
  assert_eq!(" slim", first.name, "expected name of first preset is 'slim'");
  assert_eq!(1, first.others.len(), "expected the preset slim to have one field")
}

fn verify_methods(methods : Vec<gramma::gtypes::Method>){
  let list_names = ["test"];
  let list_parm : [Vec<String>;1]= [vec![" arg1".to_string(), " arg2".to_string(), " arg3".to_string()]];
  let list_calls = [1];

  for (m, ((exp_n, exp_p), call)) in methods.iter().zip(list_names.iter().zip(list_parm.iter()).zip(list_calls)){
    assert_eq!(*exp_n, m.name, "name of method has wrong");
    assert_eq!(*exp_p, m.parameters);
    assert_eq!(call, m.calls.len(), "expected one call for thio");
  }
}