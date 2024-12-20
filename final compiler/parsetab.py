
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftTT_plusTT_subleftTT_mulTT_divrightTT_pownonassocTT_lessTT_greaterTT_leqTT_geqTT_dequTT_colon TT_comma TT_dequ TT_div TT_elif TT_else TT_equ TT_float TT_for TT_geq TT_greater TT_identifier TT_if TT_in TT_int TT_lbracket TT_leq TT_less TT_lparen TT_mul TT_plus TT_pow TT_print TT_rbracket TT_rparen TT_string TT_sub TT_whileprogram : statement_liststatement_list : statement_list statement\n                          | statementstatement : assignment\n                     | print_statement\n                     | if_statement\n                     | while_loop\n                     | for_loopassignment : TT_identifier TT_equ expression\n                      | TT_identifier TT_equ TT_float\n                      | TT_identifier TT_equ TT_intif_statement : TT_if expression TT_colon statement_list elif_clauses else_clauseelif_clauses : elif_clauses TT_elif expression TT_colon statement_list\n                        | emptyelse_clause : TT_else TT_colon statement_list\n                       | emptywhile_loop : TT_while expression TT_colon statement_listfor_loop : TT_for TT_identifier TT_in expression TT_colon statement_listexpression : expression TT_plus expression\n                      | expression TT_sub expression\n                      | expression TT_mul expression\n                      | expression TT_div expression\n                      | expression TT_pow expression\n                      | expression TT_dequ expression\n                      | expression TT_less expression\n                      | expression TT_greater expression\n                      | expression TT_leq expression\n                      | expression TT_geq expression\n                      | array_access\n                      | TT_int\n                      | TT_string\n                      | TT_float\n                      | TT_identifier\n                      | arrayarray : TT_lbracket elements TT_rbracketarray_access : TT_identifier TT_lbracket expression TT_rbracketelements : elements TT_comma expression\n                    | expression\n                    | emptyprint_statement : TT_print TT_lparen expression TT_rparen\n                           | TT_print TT_lparen TT_string TT_rparen\n                           | TT_print TT_lparen TT_float TT_rparen\n                           | TT_print TT_lparen TT_int TT_rparen\n                           | TT_print TT_lparen TT_identifier TT_rparenempty :'
    
_lr_action_items = {'TT_identifier':([0,2,3,4,5,6,7,8,11,12,13,14,15,16,18,19,20,21,22,23,24,27,28,29,35,36,37,38,39,40,41,42,43,44,45,46,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,70,71,73,74,75,77,78,79,81,82,84,85,86,87,],[9,9,-3,-4,-5,-6,-7,-8,22,22,26,-2,22,34,-29,-30,-31,-32,-33,-34,22,-9,-10,-11,9,22,22,22,22,22,22,22,22,22,22,22,9,22,-40,-41,-42,-43,-44,9,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,22,9,-45,-14,-36,9,-12,22,-16,9,9,9,9,9,]),'TT_print':([0,2,3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,35,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,77,78,81,82,84,85,86,87,],[10,10,-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,10,10,-40,-41,-42,-43,-44,10,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,10,-45,-14,-36,10,-12,-16,10,10,10,10,10,]),'TT_if':([0,2,3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,35,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,77,78,81,82,84,85,86,87,],[11,11,-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,11,11,-40,-41,-42,-43,-44,11,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,11,-45,-14,-36,11,-12,-16,11,11,11,11,11,]),'TT_while':([0,2,3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,35,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,77,78,81,82,84,85,86,87,],[12,12,-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,12,12,-40,-41,-42,-43,-44,12,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,12,-45,-14,-36,12,-12,-16,12,12,12,12,12,]),'TT_for':([0,2,3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,35,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,77,78,81,82,84,85,86,87,],[13,13,-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,13,13,-40,-41,-42,-43,-44,13,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,13,-45,-14,-36,13,-12,-16,13,13,13,13,13,]),'$end':([1,2,3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,78,81,82,86,87,],[0,-1,-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,-40,-41,-42,-43,-44,-45,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,-17,-45,-14,-36,-12,-16,-18,-15,-13,]),'TT_elif':([3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,78,81,82,86,87,],[-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,-40,-41,-42,-43,-44,-45,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,-17,79,-14,-36,-12,-16,-18,-15,-13,]),'TT_else':([3,4,5,6,7,8,14,18,19,20,21,22,23,27,28,29,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,71,73,74,75,78,81,82,86,87,],[-3,-4,-5,-6,-7,-8,-2,-29,-30,-31,-32,-33,-34,-9,-10,-11,-40,-41,-42,-43,-44,-45,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,-17,80,-14,-36,-12,-16,-18,-15,-13,]),'TT_equ':([9,],[15,]),'TT_lparen':([10,],[16,]),'TT_int':([11,12,15,16,24,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[19,19,29,33,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'TT_string':([11,12,15,16,24,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[20,20,20,31,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'TT_float':([11,12,15,16,24,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[21,21,28,32,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'TT_lbracket':([11,12,15,16,22,24,34,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[24,24,24,24,46,24,46,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'TT_colon':([17,18,19,20,21,22,23,25,58,59,60,61,62,63,64,65,66,67,69,72,75,80,83,],[35,-29,-30,-31,-32,-33,-34,50,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,77,-36,84,85,]),'TT_plus':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[36,-29,-30,-31,-32,-33,-34,36,36,-32,-30,36,-31,-32,-30,-33,36,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,36,-35,36,-36,36,36,]),'TT_sub':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[37,-29,-30,-31,-32,-33,-34,37,37,-32,-30,37,-31,-32,-30,-33,37,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,37,-35,37,-36,37,37,]),'TT_mul':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[38,-29,-30,-31,-32,-33,-34,38,38,-32,-30,38,-31,-32,-30,-33,38,38,38,-21,-22,-23,-24,-25,-26,-27,-28,38,-35,38,-36,38,38,]),'TT_div':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[39,-29,-30,-31,-32,-33,-34,39,39,-32,-30,39,-31,-32,-30,-33,39,39,39,-21,-22,-23,-24,-25,-26,-27,-28,39,-35,39,-36,39,39,]),'TT_pow':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[40,-29,-30,-31,-32,-33,-34,40,40,-32,-30,40,-31,-32,-30,-33,40,40,40,40,40,40,-24,-25,-26,-27,-28,40,-35,40,-36,40,40,]),'TT_dequ':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[41,-29,-30,-31,-32,-33,-34,41,41,-32,-30,41,-31,-32,-30,-33,41,41,41,41,41,41,None,None,None,None,None,41,-35,41,-36,41,41,]),'TT_less':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[42,-29,-30,-31,-32,-33,-34,42,42,-32,-30,42,-31,-32,-30,-33,42,42,42,42,42,42,None,None,None,None,None,42,-35,42,-36,42,42,]),'TT_greater':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[43,-29,-30,-31,-32,-33,-34,43,43,-32,-30,43,-31,-32,-30,-33,43,43,43,43,43,43,None,None,None,None,None,43,-35,43,-36,43,43,]),'TT_leq':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[44,-29,-30,-31,-32,-33,-34,44,44,-32,-30,44,-31,-32,-30,-33,44,44,44,44,44,44,None,None,None,None,None,44,-35,44,-36,44,44,]),'TT_geq':([17,18,19,20,21,22,23,25,27,28,29,30,31,32,33,34,48,58,59,60,61,62,63,64,65,66,67,68,69,72,75,76,83,],[45,-29,-30,-31,-32,-33,-34,45,45,-32,-30,45,-31,-32,-30,-33,45,45,45,45,45,45,None,None,None,None,None,45,-35,45,-36,45,45,]),'TT_rparen':([18,19,20,21,22,23,30,31,32,33,34,58,59,60,61,62,63,64,65,66,67,69,75,],[-29,-30,-31,-32,-33,-34,52,53,54,55,56,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,-36,]),'TT_rbracket':([18,19,20,21,22,23,24,47,48,49,58,59,60,61,62,63,64,65,66,67,68,69,75,76,],[-29,-30,-31,-32,-33,-34,-45,69,-38,-39,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,75,-35,-36,-37,]),'TT_comma':([18,19,20,21,22,23,24,47,48,49,58,59,60,61,62,63,64,65,66,67,69,75,76,],[-29,-30,-31,-32,-33,-34,-45,70,-38,-39,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-35,-36,-37,]),'TT_in':([26,],[51,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement_list':([0,35,50,77,84,85,],[2,57,71,82,86,87,]),'statement':([0,2,35,50,57,71,77,82,84,85,86,87,],[3,14,3,3,14,14,3,14,3,3,14,14,]),'assignment':([0,2,35,50,57,71,77,82,84,85,86,87,],[4,4,4,4,4,4,4,4,4,4,4,4,]),'print_statement':([0,2,35,50,57,71,77,82,84,85,86,87,],[5,5,5,5,5,5,5,5,5,5,5,5,]),'if_statement':([0,2,35,50,57,71,77,82,84,85,86,87,],[6,6,6,6,6,6,6,6,6,6,6,6,]),'while_loop':([0,2,35,50,57,71,77,82,84,85,86,87,],[7,7,7,7,7,7,7,7,7,7,7,7,]),'for_loop':([0,2,35,50,57,71,77,82,84,85,86,87,],[8,8,8,8,8,8,8,8,8,8,8,8,]),'expression':([11,12,15,16,24,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[17,25,27,30,48,58,59,60,61,62,63,64,65,66,67,68,72,76,83,]),'array_access':([11,12,15,16,24,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'array':([11,12,15,16,24,36,37,38,39,40,41,42,43,44,45,46,51,70,79,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'elements':([24,],[47,]),'empty':([24,57,73,],[49,74,81,]),'elif_clauses':([57,],[73,]),'else_clause':([73,],[78,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',133),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','parser.py',138),
  ('statement_list -> statement','statement_list',1,'p_statement_list','parser.py',139),
  ('statement -> assignment','statement',1,'p_statement','parser.py',147),
  ('statement -> print_statement','statement',1,'p_statement','parser.py',148),
  ('statement -> if_statement','statement',1,'p_statement','parser.py',149),
  ('statement -> while_loop','statement',1,'p_statement','parser.py',150),
  ('statement -> for_loop','statement',1,'p_statement','parser.py',151),
  ('assignment -> TT_identifier TT_equ expression','assignment',3,'p_assignment','parser.py',156),
  ('assignment -> TT_identifier TT_equ TT_float','assignment',3,'p_assignment','parser.py',157),
  ('assignment -> TT_identifier TT_equ TT_int','assignment',3,'p_assignment','parser.py',158),
  ('if_statement -> TT_if expression TT_colon statement_list elif_clauses else_clause','if_statement',6,'p_if_statement','parser.py',167),
  ('elif_clauses -> elif_clauses TT_elif expression TT_colon statement_list','elif_clauses',5,'p_elif_clauses','parser.py',172),
  ('elif_clauses -> empty','elif_clauses',1,'p_elif_clauses','parser.py',173),
  ('else_clause -> TT_else TT_colon statement_list','else_clause',3,'p_else_clause','parser.py',181),
  ('else_clause -> empty','else_clause',1,'p_else_clause','parser.py',182),
  ('while_loop -> TT_while expression TT_colon statement_list','while_loop',4,'p_while_loop','parser.py',190),
  ('for_loop -> TT_for TT_identifier TT_in expression TT_colon statement_list','for_loop',6,'p_for_loop','parser.py',195),
  ('expression -> expression TT_plus expression','expression',3,'p_expression','parser.py',200),
  ('expression -> expression TT_sub expression','expression',3,'p_expression','parser.py',201),
  ('expression -> expression TT_mul expression','expression',3,'p_expression','parser.py',202),
  ('expression -> expression TT_div expression','expression',3,'p_expression','parser.py',203),
  ('expression -> expression TT_pow expression','expression',3,'p_expression','parser.py',204),
  ('expression -> expression TT_dequ expression','expression',3,'p_expression','parser.py',205),
  ('expression -> expression TT_less expression','expression',3,'p_expression','parser.py',206),
  ('expression -> expression TT_greater expression','expression',3,'p_expression','parser.py',207),
  ('expression -> expression TT_leq expression','expression',3,'p_expression','parser.py',208),
  ('expression -> expression TT_geq expression','expression',3,'p_expression','parser.py',209),
  ('expression -> array_access','expression',1,'p_expression','parser.py',210),
  ('expression -> TT_int','expression',1,'p_expression','parser.py',211),
  ('expression -> TT_string','expression',1,'p_expression','parser.py',212),
  ('expression -> TT_float','expression',1,'p_expression','parser.py',213),
  ('expression -> TT_identifier','expression',1,'p_expression','parser.py',214),
  ('expression -> array','expression',1,'p_expression','parser.py',215),
  ('array -> TT_lbracket elements TT_rbracket','array',3,'p_array','parser.py',228),
  ('array_access -> TT_identifier TT_lbracket expression TT_rbracket','array_access',4,'p_array_access','parser.py',233),
  ('elements -> elements TT_comma expression','elements',3,'p_elements','parser.py',238),
  ('elements -> expression','elements',1,'p_elements','parser.py',239),
  ('elements -> empty','elements',1,'p_elements','parser.py',240),
  ('print_statement -> TT_print TT_lparen expression TT_rparen','print_statement',4,'p_print_statement','parser.py',250),
  ('print_statement -> TT_print TT_lparen TT_string TT_rparen','print_statement',4,'p_print_statement','parser.py',251),
  ('print_statement -> TT_print TT_lparen TT_float TT_rparen','print_statement',4,'p_print_statement','parser.py',252),
  ('print_statement -> TT_print TT_lparen TT_int TT_rparen','print_statement',4,'p_print_statement','parser.py',253),
  ('print_statement -> TT_print TT_lparen TT_identifier TT_rparen','print_statement',4,'p_print_statement','parser.py',254),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',266),
]
