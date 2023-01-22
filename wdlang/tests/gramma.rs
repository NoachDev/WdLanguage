use wdlang::gramma;
use std::path::Path;

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

  verify_wdigets(ret.widgets);
  verify_vars(repo.wd_vars);
  verify_presets(repo.presets);
  verify_methods(ret.methods);

  assert_eq!(Some(func.join("__init__.py")), ret.script);

}

fn verify_wdigets(widgets : Vec<gramma::gtypes::Widget>){
  assert_eq!(widgets.len(), 2);

  let wd_0 = &widgets[0];

  assert_eq!(wd_0.name, "__master__");
  assert_eq!(wd_0.commands.len(), 3);

  let wd_1 = &widgets[1];

  assert_eq!("f_test", wd_1.name, "expected 'f_test' of name in second widget");
  assert_eq!(Some(" Button".to_string()), wd_1.element_type, "expected Frame of type on second widget");

  assert_eq!(wd_1.presets.len(), 1, "expeted one presets on second widget");
  assert!(wd_1.presets[0].name == " slim", "expected to have slim in second widget");

  assert_eq!(3, wd_1.atributs.len(), "expected 3 atributes on second wdiget");
  assert_eq!(1, wd_1.commands.len(), "expected 1 command on second widget");   

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