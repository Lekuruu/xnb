
from enum import IntEnum

class SurfaceFormat(IntEnum):
    Color = 0
    Bgr565 = 1
    Bgra5551 = 2
    Bgra4444 = 3
    Dxt1 = 4
    Dxt3 = 5
    Dxt5 = 6
    NormalizedByte2 = 7
    NormalizedByte4 = 8
    Rgba1010102 = 9
    Rg32 = 10
    Rgba64 = 11
    Alpha8 = 12
    Single = 13
    Vector2 = 14
    Vector4 = 15
    HalfSingle = 16
    HalfVector2 = 17
    HalfVector4 = 18
    HdrBlendable = 19
    Bgr32 = 20
    Bgra32 = 21
    ColorSRgb = 30
    Bgr32SRgb = 31
    Bgra32SRgb = 32
    Dxt1SRgb = 33
    Dxt3SRgb = 34
    Dxt5SRgb = 35
    RgbPvrtc2Bpp = 50
    RgbPvrtc4Bpp = 51
    RgbaPvrtc2Bpp = 52
    RgbaPvrtc4Bpp = 53
    RgbEtc1 = 60
    Dxt1a = 70
    RgbaAtcExplicitAlpha =  80
    RgbaAtcInterpolatedAlpha = 81
    Rgb8Etc2 = 90
    Srgb8Etc2 = 91
    Rgb8A1Etc2 = 92
    Srgb8A1Etc2 = 93
    Rgba8Etc2 = 94
    SRgb8A8Etc2 = 95
