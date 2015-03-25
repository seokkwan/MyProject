# -*- coding: utf-8 -*

'''
File: quick_select_export.py

Author: Lee Seok Kwan

Contact: leesk004@naver.com

Versions:
1.0 - 03/06/2015 - first version created

How to use:

1. Place script in :
    C:/Users/yourUserName/Documents/maya/2013-x64/scripts/
    
2. workflow:
    - export 할 오브젝트를 선택해서 실행

3. To run tool:
    import quick_select_export
    reload(quick_select_export)
    quick_select_export.ExportObject('mb')

'''

import pymel.core as pm
import logging

class ExportObject:
    fileTypes = {'mb': 'mayaBinary', 'ma': 'mayaAscii'}
    def __init__(self, type):
        self.type = type
        self.sName = pm.Env().sceneName().dirname() + '/'
        window_name = 'export_object'
        try:
            pm.deleteUI(window_name)
        except:
            pass
        with pm.window(window_name, title='Export Object'):
            with pm.columnLayout(adj=True, cat=('both', 5), rs=2):
                # Export Path
                pm.separator(style='in', h=2)
                with pm.rowColumnLayout(nc=3, cw=[(1, 50), (2, 270), (3, 80)],
                                        cat=[(1, 'both', 2), (2, 'both', 5), (3, 'both', 5)]):
                    pm.text(label='Path :')
                    self.pathTF = pm.textField(text=self.sName)
                    pm.button(label='Set', command=self.export_dir_set)
                pm.separator(style='in', h=2)
                # Include Options
                with pm.columnLayout(adj=True, cat=('both', 5)):
                    self.includeAllCB = pm.checkBox(label='Include these inputs :', value=1,
                                                    offCommand=pm.Callback(self.optionCheck, 'off'),
                                                    onCommand =pm.Callback(self.optionCheck, 'on'))
                with pm.columnLayout(adj=True, cat=('left', 40), rs=2):
                    self.historyCB = pm.checkBox(label='History', value=1, align='right')
                    self.channelsCB = pm.checkBox(label='Channels', value=1)
                    self.expressionsCB = pm.checkBox(label='Expressions', value=1)
                    self.constraintsCB = pm.checkBox(label='Constraints', value=1)
                pm.separator(style='in', h=2)
                with pm.rowColumnLayout(nc=2, cw=[(1, 200), (2, 200)],
                                        cat=[(1, 'both', 3), (2, 'both', 3)]):
                    pm.button(label='Export', command=pm.Callback(self.file_export, self.type))
                    pm.button(label='Close', h=30, command=pm.Callback(pm.deleteUI, window_name))
                    pm.text(label='leesk004@naver.com', align='left')
                    pm.text(label='by Lee Seok Kwan', align='right')
        pm.window(window_name, edit=True, width=400, height=190)

    def export_dir_set(self, *args):
        '''
        익스포트 디렉토리 경로를 사용자 정의 합니다.
        :param args:
        :return:
        '''
        current_path = self.pathTF.getText()
        listDir = pm.fileDialog2(dialogStyle=1, fileMode=3, okc='Set', cc='Cancel', dir=current_path)
        try:
            current_path = '{path}/'.format(path=listDir[0].replace('\\', '/'))
            self.pathTF.setText(current_path)
        except:
            pass

    def optionCheck(self, check):
        '''
        익스포트 옵션 체크
        :param check: off/on
        :return:
        '''
        if check == 'on':
            self.historyCB.setValue(1)
            self.channelsCB.setValue(1)
            self.expressionsCB.setValue(1)
            self.constraintsCB.setValue(1)
        elif check == 'off':
            self.historyCB.setValue(0)
            self.channelsCB.setValue(0)
            self.expressionsCB.setValue(0)
            self.constraintsCB.setValue(0)

    def file_export(self, type):
        '''
        선택한 오브젝트를 익스포트 합니다.
        :param type: 익스포트 타입 'mb', 'ma'
        :return:
        '''
        objects = pm.selected()
        if objects:
            hi = self.historyCB.getValue()
            ch = self.channelsCB.getValue()
            ex = self.expressionsCB.getValue()
            ct = self.constraintsCB.getValue()
            export_objects = [x for x in objects if pm.nodeType(x.getShapes()[0]) == 'mesh' or pm.nodeType(x) == 'transform']
            try:
                file_name = export_objects[0].name()
                full_path = '{path}{name}.{ender}'.format(path=self.pathTF.getText(), name=file_name, ender=type)
                pm.exportSelected(full_path,
                                  constructionHistory=hi,
                                  channels=ch,
                                  expressions=ex,
                                  constraints=ct,
                                  type=self.fileTypes[type])
            except:
                pass
        else:
            logging.error(u'오브젝트를 선택하세요~!!')