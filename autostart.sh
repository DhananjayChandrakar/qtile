#!/bin/sh
/usr/share/pipewire &
/usr/share.pipewire-pulse &
/usr/bin/pipewire-media-session &
nitrogen --restore &
picom &
