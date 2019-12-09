#ifndef _TRANSFORM
#define _TRANSFORM

class Transform {
    public:
        static float degToRad(float angle_deg);
        static float radToDeg(float angle_rad);
        static float getSolidAngle(
            float theta_nad_min = THETA_NADIR_MIN, float theta_nad_max = THETA_NADIR_MAX,
            float phi_nad_min = PHI_NADIR_MIN, float phi_nad_max = PHI_NADIR_MAX
        );
};

#endif