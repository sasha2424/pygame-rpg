


class Render_Queue:

    render_list = []

def queue_render(y,*args):
    Render_Queue.render_list.append((y,args))
