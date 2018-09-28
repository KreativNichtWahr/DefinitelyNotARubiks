import math
from glumpy import app, gloo, gl


# That is how a rotation around the origin works

#Derive the formula for rotation
#(old coordinates are (x, y) and the new coordinates are (x', y'))

#q = initial angle, f = angle of rotation.

#x = r cos q
#y = r sin q

#x' = r cos ( q + f ) = r cos q cos f - r sin q sin f
#y' = r sin ( q + w ) = r sin q cos f + r cos q sin f

#hence:
#x' = x cos f - y sin f
#y' = y cos f + x sin f



if __name__ == "__main__":
    vertex = """
        attribute vec2 position;
        attribute vec4 color;
        uniform float theta;
        varying vec4 v_color;
        void main() {
            float c = cos(theta);
            float s = sin(theta);
            float x = c*position.x - s*position.y;
            float y = s*position.x + c*position.y;
            gl_Position = vec4(0.7*vec2(x,y), 0.0, 1.0);
            v_color = color;
        } """

    fragment = """
        varying vec4 v_color;
        void main() { gl_FragColor = v_color; } """


    window = app.Window(color=(1,1,1,1))
    quad = gloo.Program(vertex, fragment, count=4)
    quad['position'] = (-1,+1), (+1,+1), (-1,-1), (+1,-1)
    quad['color'] = (1,1,0,1), (1,0,0,1), (0,0,1,1), (0,1,0,1)

    angle = 0.0

    @window.event
    def on_draw(dt):
        global angle
        angle += 1.0 * math.pi/180.0
        window.clear()
        quad["theta"] = angle
        quad.draw(gl.GL_TRIANGLE_STRIP)

    # We set the framecount to 360 in order to record a movie that can
    # loop indefinetly. Run this program with:
    # python quad-scale.py --record quad-scale.mp4
    app.run()
