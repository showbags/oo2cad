import bpy
import importlib
import os.path
import play
import lib
import shapes

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    _last_play_mod = None
    _last_lib_mod = None
    _last_shapes_mod = None

    def updatePlay(self):
        mod = os.path.getmtime('modules/play.py')
        if self._last_play_mod is None or mod>self._last_play_mod:
            importlib.reload(play)
            self._last_play_mod=mod
            return True
        return False

    def updateLib(self):
        mod = os.path.getmtime('modules/lib.py')
        if self._last_lib_mod is None or mod>self._last_lib_mod:
            importlib.reload(lib)
            self._last_lib_mod=mod
            return True
        return False

    def updateShapes(self):
        mod = os.path.getmtime('modules/shapes.py')
        if self._last_shapes_mod is None or mod>self._last_shapes_mod:
            importlib.reload(shapes)
            self._last_shapes_mod=mod
            return True
        return False

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self.updatePlay() or self.updateLib() or self.updateShapes():
                importlib.reload(play)
                importlib.reload(lib)
                importlib.reload(shapes)
                play.run()
                print("doing it")

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.5, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

def menu_func(self, context):
  self.layout.operator(ModalTimerOperator.bl_idname, text=ModalTimerOperator.bl_label)

def register():
  bpy.utils.register_class(ModalTimerOperator)
  bpy.types.VIEW3D_MT_view.append(menu_func)

# Register and add to the "view" menu (required to also use F3 search "Modal Timer Operator" for quick access)
def unregister():
  bpy.utils.unregister_class(ModalTimerOperator)
  bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
  register()

  # test call
  bpy.ops.wm.modal_timer_operator()
