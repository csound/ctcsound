require(['notebook/js/codecell'], function(codecell) {
  codecell.CodeCell.options_default.highlight_modes['magic_csound'] = {'reg':[/^%%csound/, /^%%csd/, /^%%orc/, /^%%sco/]};
});
