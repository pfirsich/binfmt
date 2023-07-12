# binfmt

Builds binary files from text descriptions, e.g.:
```
#      x    y   z          u      v
f32 -1.0 -1.0 0.0 u16 0xffff 0x0000
f32 -1.0  1.0 0.0 u16 0xffff 0x0000
f32  1.0  1.0 0.0 u16 0x0000 0x0000
f32  1.0 -1.0 0.0 u16 0x0000 0xffff
```
