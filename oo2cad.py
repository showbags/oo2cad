import bpy
import importlib
import os.path
import play

class ModalTimerOperator(bpy.types.Operator):
  """Operator which runs its self from a timer"""
  bl_idname = "wm.modal_timer_operator"
  bl_label = "Modal Timer Operator"

  _timer = None
  _last_mod = None

  def modal(self, context, event):
    if event.type == 'TIMER':
      mod = os.path.getmtime('modules/play.py')
      if self._last_mod is None or mod>self._last_mod:
        importlib.reload(play)
        play.run()
        self._last_mod=mod

    return {'PASS_THROUGH'}

  def execute(self, context):
    wm = context.window_manager
    self._timer = wm.event_timer_add(3, window=context.window)
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
