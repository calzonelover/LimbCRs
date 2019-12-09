#ifndef _TRANSFORM
#define _TRANSFORM

class Transform {
    public:
        static float degToRad(float angle_deg);
        static float radToDeg(float angle_rad);
        static float getSolidAngle(float theta_nad_min, float theta_nad_max, float phi_nad_min, float phi_nad_max);
}

#endif