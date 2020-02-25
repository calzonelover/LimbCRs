#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <math.h>

#include "../../settings.h"
#include "../../utility/cpp/parser.h"

#include "transform.h"

float Transform::degToRad(float angle_deg){
    return angle_deg * PI / 180.0f;
}

float Transform::radToDeg(float angle_rad){
    return angle_rad * 180.0f / PI;
}

float Transform::getSolidAngle(
        float phi_nad_min, float phi_nad_max,
        float theta_nad_min, float theta_nad_max
    ){
    auto out = (cos(degToRad(theta_nad_min)) - cos(degToRad(theta_nad_max))) * degToRad(phi_nad_max - phi_nad_min);
    return out;
}