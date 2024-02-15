#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#import csv

from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, BooleanField#, FieldList 
#from wtforms import StringField, BooleanField, SelectField
from wtforms import validators

def cell_name(k):
    return f"cell_{'_'.join([str(c) for c in coord])}"

def create_radio_enrollment_class(options_dict, row_names, col_names):
    class Form(FlaskForm):
        @staticmethod
        def html_field_name(tup):
            return f"cell_{'_'.join([str(c) for c in tup])}"
        
        @staticmethod
        def html_description(tup):
            h_coord, d_coord = tup
            time_str = f'{" a ".join(row_names[h_coord])}'
            day_str = col_names[d_coord]
            return f'{day_str} de {time_str}'

        @staticmethod
        def key_tuple(name):
            _,a,b = name.split('_')
            return int(a), int(b)

    for coord in sorted(options_dict.keys(),
                        key = lambda x: (x[1], x[0])):
        name = Form.html_field_name(coord)
        setattr(Form, name, RadioField(
            name,
            validators=[validators.InputRequired('↑ Selecciona una opción')],
            choices=options_dict[coord],
            description=Form.html_description(coord)))
    #setattr(Form, 'submit', SubmitField('Continuar ->'))
    return Form
        
def create_switched_enrollment_class(df, row_names, col_names):
    class Form(FlaskForm):
        @staticmethod
        def html_field_name(idx):
            return f"ws_{idx}"
        
        @staticmethod
        def html_description(tup, short=False):
            h_coord, d_coord = tup
            day_str = col_names[d_coord]
            if short:
                text = day_str
            else:
                time_str = f'{" a ".join(row_names[h_coord])}'
                text = f'{day_str} de {time_str}'
            return text

        @staticmethod
        def name_idx(name):
            return int(name.split('_')[1])
        
    #Grouping form fields in form.groups dict.
    #Dict values are two keys dicts with inputs labels and texts that don't use inputs.
    #form.groups
    #{'<Day and time str>': {'inputs': [<input label>, ...] , 'texts': [<text>, ...]} }
        def daytime_grouping(self):
            kfmt = Form.html_description
            t = self.df
            g = t.groupby([t.coords.str[0].str[1], t.coords.str[0].str[0]]).groups
            g = {kfmt((k[1],k[0])): [
                    getattr(self, self.html_field_name(i)) for i in v ]
                for k,v in g.items() }
            all_g = {kfmt((a,b)): {'inputs': [], 'texts': []}
                     for b in range(len(self.col_names))
                     for a in range(len(self.row_names))
                      }
            for k in all_g:
                if k in g:
                    all_g[k]['inputs'] = g[k]
            for i in t.index:
                if len(t.loc[i].coords) > 1:
                    for coord in t.loc[i].coords[1:]:
                        text = f"({t.loc[i, 'name']} con {t.loc[i, 'teacher']})"
                        all_g[kfmt(coord)]['texts'].append(text)
            self.groups = all_g
    
    setattr(Form,'row_names', row_names)
    setattr(Form, 'col_names', col_names)
    setattr(Form, 'df', df)
    for idx in df.index:
        name = Form.html_field_name(idx)
        s = df.loc[idx]
        horarios = ' y '.join([
            Form.html_description(t, short=True) for t in s.coords])
        lb = f'{s["name"]} con {s.teacher} ({horarios}).'
        setattr(Form, name, BooleanField(
            label = lb,
            id = name,
            description=s.loc['description']))
    return Form

#if __name__ == '__main__':
    #pass
