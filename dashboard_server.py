# -*- coding: utf-8 -*-
"""
FreeFire Level Up Bot - Professional Web Dashboard & Real-Time EXP Tracker
Embedded Async Web Server (aiohttp)
"""

import asyncio
import json
import os
import time

# Account level eta ba tar beshi hole BR theke automatic Lone Wolf. 0 dile bondho.
try:
    AUTO_LW_LEVEL = int(os.environ.get("AUTO_LW_LEVEL", "3"))
except Exception:
    AUTO_LW_LEVEL = 3
from typing import Dict, List, Any, Optional
from aiohttp import web

# ==================== BASE DIRECTORY (ALWAYS ABSOLUTE) ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ✅ AUTO MULTI-FILE SUPPORT - accounts.json, accounts2.json, accounts3.json ...
import glob as _glob

def get_all_account_files_dashboard():
    """Root-এ accounts*.json সব ফাইল অটো ডিটেক্ট করে"""
    files = sorted(_glob.glob(os.path.join(BASE_DIR, "accounts*.json")))
    if not files:
        files = [os.path.join(BASE_DIR, "accounts.json")]
    return files

ACCOUNTS_FILE_PATH = os.path.join(BASE_DIR, "accounts.json")  # default for new adds

# ==================== EMBEDDED HTML DASHBOARD ====================
# HTML is embedded directly — no external file dependency (works on Termux/mobile)
DASHBOARD_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#000000">
<title>ARAFAT FLEX — Level Up</title>
<link rel="icon" href="/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@500;600;700&family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>
:root{--bg:#000;--g1:#0b0b0b;--g2:#141414;--g3:#1d1d1d;--ln:rgba(255,255,255,.08);--red:#ff1a1a;--rg:rgba(255,26,26,.38);--tx:#fff;--tx2:#bdbdbd;--mut:#7a7a7a;--ok:#2bff88;--amb:#ffb020;--fd:'Orbitron','Rajdhani',sans-serif;--fr:'Rajdhani','Segoe UI',sans-serif;--fb:'Space Grotesk',system-ui,sans-serif;--e:cubic-bezier(.2,.8,.2,1)}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{max-width:100%;overflow-x:hidden}
body{font-family:var(--fb);background:#000;color:var(--tx);min-height:100vh;-webkit-font-smoothing:antialiased;font-size:14px;font-variant-numeric:tabular-nums;background-image:radial-gradient(60% 40% at 50% -10%,rgba(255,26,26,.2),transparent 70%),radial-gradient(40% 30% at 100% 100%,rgba(255,26,26,.09),transparent 70%)}
body::before{content:'';position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:48px 48px;-webkit-mask-image:radial-gradient(ellipse at 50% 0,#000,transparent 75%);mask-image:radial-gradient(ellipse at 50% 0,#000,transparent 75%)}
button,input,select{font:inherit;color:inherit}button{cursor:pointer}
[hidden]{display:none!important}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-thumb{background:#2a2a2a;border-radius:99px}::-webkit-scrollbar-thumb:hover{background:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes up{from{opacity:0;translate:0 18px}to{opacity:1;translate:0 0}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 currentColor}50%{box-shadow:0 0 0 6px transparent}}
@keyframes shim{to{background-position:-200% 0}}
.stg{animation:up .7s var(--e) both;animation-delay:calc(var(--i,0)*80ms)}

.app{position:relative;z-index:1;display:grid;grid-template-columns:330px 1fr;grid-template-rows:68px 1fr;height:100vh;height:100dvh}
.header{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 22px;background:rgba(0,0,0,.72);border-bottom:1px solid rgba(255,26,26,.28);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);z-index:100;box-shadow:0 1px 30px rgba(255,26,26,.12)}
.brand{display:flex;align-items:center;gap:12px;min-width:0;flex:1}
.brand>div{min-width:0}
.logo{position:relative;width:46px;height:46px;flex:0 0 auto;border-radius:50%;padding:2px}
.logo::before{content:'';position:absolute;inset:0;border-radius:50%;background:conic-gradient(var(--red),transparent 40%,#fff 55%,transparent 70%,var(--red));animation:spin 4s linear infinite}
.logo img{position:relative;width:100%;height:100%;border-radius:50%;object-fit:cover;border:2px solid #000;display:block}
.brand-name{font-family:var(--fd);font-weight:900;font-size:19px;letter-spacing:.06em;font-style:italic;transform:skewX(-8deg);transform-origin:left;white-space:nowrap;text-shadow:0 0 20px var(--rg);overflow:hidden;text-overflow:ellipsis}
.brand-sub{font-family:var(--fr);font-size:14px;font-weight:600;color:var(--mut);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.header-right{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.rolechip{font-family:var(--fr);font-size:13px;font-weight:700;padding:3px 12px;border-radius:99px;border:1px solid rgba(255,26,26,.5);color:var(--red);background:rgba(255,26,26,.08)}
.live{display:flex;align-items:center;gap:8px;font-family:var(--fr);font-size:14px;font-weight:700;color:var(--ok);white-space:nowrap}
.live i{width:9px;height:9px;border-radius:50%;background:currentColor;animation:pulse 1.8s ease-in-out infinite}
.live.off{color:var(--red)}.live.off i{animation:none}
.btn-primary,.btn-ghost,.btn-block,.btn-icon{transition:transform .15s,box-shadow .25s,border-color .25s,background .25s}
.btn-primary{height:44px;padding:0 20px;background:linear-gradient(100deg,#d90000,var(--red));color:#fff;border:0;border-radius:12px;font-family:var(--fr);font-size:16px;font-weight:700;letter-spacing:.04em;display:flex;align-items:center;justify-content:center;gap:8px;white-space:nowrap;box-shadow:0 6px 24px rgba(255,26,26,.35)}
.btn-primary:hover{box-shadow:0 8px 34px rgba(255,26,26,.6);transform:translateY(-1px)}.btn-primary:active{transform:scale(.97)}
.btn-primary:disabled{opacity:.6;cursor:wait}
.btn-icon{width:44px;height:44px;flex:0 0 auto;display:grid;place-items:center;background:var(--g2);border:1px solid var(--ln);border-radius:12px;color:var(--tx2)}
.btn-icon:hover{color:#fff;border-color:var(--red);box-shadow:0 0 20px var(--rg)}.btn-icon svg{width:18px;height:18px}

.glass,.exp-hero,.stat-card,.row-between,.mode-row,.log-box,.acard,.modal{background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.012));border:1px solid rgba(255,26,26,.16);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:0 10px 40px rgba(0,0,0,.55)}
.sidebar{padding:16px;overflow-y:auto;display:flex;flex-direction:column;gap:16px;border-right:1px solid var(--ln);background:rgba(0,0,0,.35)}
.slabel{font-family:var(--fr);font-size:14px;font-weight:700;color:var(--tx2);letter-spacing:.04em;margin-bottom:8px}
.exp-hero{border-radius:18px;padding:18px 14px;text-align:center;position:relative;overflow:hidden}
.exp-hero::after{content:'';position:absolute;left:10%;right:10%;bottom:0;height:2px;background:linear-gradient(90deg,transparent,var(--red),transparent);box-shadow:0 0 18px var(--red)}
.exp-hero-num{font-family:var(--fd);font-weight:900;font-style:italic;font-size:clamp(30px,9vw,40px);line-height:1.05;transform:skewX(-8deg);text-shadow:0 0 28px var(--rg);word-break:break-all}
.exp-hero-num small{font-size:13px;color:var(--red);margin-right:8px;letter-spacing:.1em}
.exp-hero-sub{font-family:var(--fr);font-weight:600;font-size:15px;color:var(--tx2);margin-top:8px;min-height:1.2em}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.stat-card{border-radius:14px;padding:12px 14px;position:relative;overflow:hidden;transition:border-color .25s,box-shadow .25s}
.stat-card:hover{border-color:rgba(255,26,26,.6);box-shadow:0 0 28px rgba(255,26,26,.22)}
.stat-card.wide{grid-column:1/-1}
.stat-card:has(.c-green)::after{content:'';position:absolute;top:14px;right:14px;width:8px;height:8px;border-radius:50%;background:var(--ok);color:var(--ok);animation:pulse 1.8s infinite}
.stat-card:has(.c-amber)::after{content:'';position:absolute;top:14px;right:14px;width:8px;height:8px;border-radius:50%;background:var(--amb);color:var(--amb);animation:pulse 1.4s infinite}
.stat-num{font-family:var(--fr);font-size:30px;font-weight:700;line-height:1;min-height:1em}
.c-fire{color:#fff}.c-green{color:#fff}.c-amber{color:#fff}.c-red{color:var(--red)}.c-muted{color:var(--tx2)}
.stat-lbl{font-size:13px;color:var(--mut);margin-top:3px}
.divider{height:1px;background:var(--ln)}
.ctrl-toggle{display:none}
.ctrl-stack{display:flex;flex-direction:column;gap:14px}
.row-between{display:flex;align-items:center;justify-content:space-between;border-radius:12px;padding:8px 14px;min-height:48px}
.row-label{font-weight:500}
.tgl{position:relative;width:52px;height:30px;flex:0 0 auto}.tgl input{opacity:0;width:100%;height:100%;position:absolute;inset:0;z-index:2;cursor:pointer;margin:0}
.tgl-track{position:absolute;inset:0;background:#222;border-radius:99px;transition:background .25s,box-shadow .25s}
.tgl-track::before{content:'';position:absolute;width:22px;height:22px;left:4px;top:4px;background:#fff;border-radius:50%;transition:transform .25s var(--e)}
.tgl input:checked+.tgl-track{background:var(--red);box-shadow:0 0 20px var(--rg)}.tgl input:checked+.tgl-track::before{transform:translateX(22px)}
.tgl input:focus-visible+.tgl-track{outline:2px solid #fff;outline-offset:2px}
.mode-row{display:grid;grid-template-columns:repeat(3,1fr);border-radius:12px;overflow:hidden}
.mbtn{min-height:44px;padding:8px 4px;font-family:var(--fr);font-size:15px;font-weight:700;background:transparent;color:var(--tx2);border:0;transition:background .2s,color .2s}
.mbtn:not(:last-child){border-right:1px solid var(--ln)}
.mbtn:hover{background:rgba(255,26,26,.08);color:#fff}
.mbtn.active{background:var(--red);color:#fff;box-shadow:0 0 22px var(--rg)}
.input-row{display:flex;gap:8px}
.inp{flex:1;min-width:0;height:44px;background:rgba(0,0,0,.6);border:1px solid var(--ln);border-radius:12px;padding:0 14px;color:#fff;font-size:16px;outline:0;transition:border-color .2s,box-shadow .2s}
.inp:focus{border-color:var(--red);box-shadow:0 0 0 3px rgba(255,26,26,.15),0 0 22px rgba(255,26,26,.15)}.inp::placeholder{color:#555}
select.inp{appearance:none;-webkit-appearance:none}select.inp option{background:#111}
.hint{min-height:1.3em;font-size:12.5px;color:var(--mut);margin-top:6px}
.btn-ghost{min-height:44px;padding:0 18px;background:var(--g2);border:1px solid var(--ln);color:#fff;border-radius:12px;font-family:var(--fr);font-size:15px;font-weight:700;white-space:nowrap}
.btn-ghost:hover{border-color:var(--red);box-shadow:0 0 18px var(--rg)}
.btn-block{width:100%;min-height:44px;background:rgba(255,26,26,.08);border:1px solid rgba(255,26,26,.4);color:#fff;border-radius:12px;font-family:var(--fr);font-size:15px;font-weight:700}
.btn-block:hover{background:rgba(255,26,26,.18);box-shadow:0 0 22px var(--rg)}.btn-block:disabled,.btn-ghost:disabled{opacity:.5;cursor:wait}

.main{overflow-y:auto;padding:20px 24px 32px;display:flex;flex-direction:column;gap:22px;min-width:0}
section{scroll-margin-top:76px}
.sec-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px;flex-wrap:wrap}
.sec-title{font-family:var(--fd);font-weight:900;font-style:italic;font-size:20px;letter-spacing:.04em;transform:skewX(-8deg);transform-origin:left}
.sec-title small{font-family:var(--fr);font-style:normal;font-size:15px;color:var(--red);margin-left:10px;display:inline-block;transform:skewX(8deg);letter-spacing:0}
.search{width:260px;max-width:100%;flex:0 1 260px}
.accounts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px;perspective:1200px}
.acard{--rx:0deg;--ry:0deg;--mx:50%;--my:0%;border-radius:18px;padding:14px;position:relative;overflow:hidden;transform:rotateX(var(--rx)) rotateY(var(--ry));transition:transform .18s ease-out,border-color .25s,box-shadow .25s;will-change:transform;animation:up .6s var(--e) both}
.acard::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--c,var(--red)),transparent)}
.acard::after{content:'';position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .25s;background:radial-gradient(260px circle at var(--mx) var(--my),rgba(255,26,26,.18),transparent 60%)}
.acard:hover{border-color:rgba(255,26,26,.65);box-shadow:0 0 34px rgba(255,26,26,.28),0 14px 40px rgba(0,0,0,.6)}.acard:hover::after{opacity:1}
.st-online{--c:var(--ok)}.st-connecting{--c:var(--amb)}.st-offline{--c:#555}.st-paused{--c:#444}
.st-match{--c:var(--red);border-color:rgba(255,26,26,.55);animation:up .6s var(--e) both,glow 2.4s ease-in-out infinite .7s}
@keyframes glow{50%{box-shadow:0 0 36px rgba(255,26,26,.4),0 10px 40px rgba(0,0,0,.55)}}
.card-top{display:flex;gap:12px;margin-bottom:12px}
.avatar{min-width:54px;height:54px;padding:0 8px;border-radius:14px;background:#000;border:1px solid rgba(255,26,26,.5);display:flex;align-items:center;justify-content:center;flex:0 0 auto;box-shadow:inset 0 0 16px rgba(255,26,26,.18)}
.lvl{font-family:var(--fd);font-weight:900;font-size:22px;display:flex;align-items:flex-end;gap:2px;line-height:1}
.lvl-tag{font-family:var(--fr);font-size:12px;color:var(--red);margin-bottom:2px}
.card-info{flex:1;min-width:0}
.nick{font-family:var(--fr);font-size:19px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;line-height:1.1}
.uid{font-size:13px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.badge-row{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
.badge{font-family:var(--fr);font-size:13px;font-weight:700;padding:2px 9px;border-radius:99px;border:1px solid var(--ln);background:rgba(255,255,255,.05);white-space:nowrap}
button.badge{min-height:28px;cursor:pointer}button.badge:hover{border-color:var(--red);background:rgba(255,26,26,.12)}
.b-online{color:var(--ok);border-color:rgba(43,255,136,.35);background:rgba(43,255,136,.08)}
.b-match{color:#fff;background:var(--red);border-color:var(--red);box-shadow:0 0 14px var(--rg)}
.b-connecting{color:var(--amb);border-color:rgba(255,176,32,.35);background:rgba(255,176,32,.08)}
.b-offline,.b-paused{color:var(--mut)}
.b-br,.b-lw{color:#fff;border-color:rgba(255,26,26,.4);background:rgba(255,26,26,.1)}
.exp-row{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.ring-wrap{position:relative;width:52px;height:52px;flex:0 0 auto}
.ring-svg{transform:rotate(-90deg);width:100%;height:100%}
.ring-bg{fill:none;stroke:#1f1f1f;stroke-width:4.5}
.ring-fill{fill:none;stroke:url(#expGrad);stroke-width:4.5;stroke-linecap:round;transition:stroke-dashoffset 1.2s var(--e);filter:drop-shadow(0 0 4px var(--red))}
.ring-pct{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--fr);font-size:14px;font-weight:700}
.exp-lbl{font-size:12.5px;color:var(--mut)}
.exp-val{font-family:var(--fr);font-size:26px;font-weight:700;line-height:1.05;color:#fff;text-shadow:0 0 16px var(--rg);white-space:nowrap}
.exp-need{font-size:12.5px;color:var(--tx2);white-space:nowrap}
.limit{height:5px;background:#1a1a1a;border-radius:99px;overflow:hidden;margin:0 0 12px}
.limit i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,#8a0000,var(--red),#ff7a7a,var(--red));background-size:200% 100%;animation:shim 2.2s linear infinite;transition:width .9s var(--e);box-shadow:0 0 12px var(--red)}
.meta{font-size:13px;color:var(--tx2);line-height:1.55;margin-bottom:10px}
.meta b{color:#fff}
.note{font-size:13px;line-height:1.4;padding:8px 10px;border-radius:10px;margin-bottom:10px;word-break:break-word;color:var(--tx2);background:rgba(255,255,255,.04);border:1px solid var(--ln);overflow:hidden;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical}
.note.err{color:#ff8a8a;background:rgba(255,26,26,.08);border-color:rgba(255,26,26,.3)}
.card-btns{display:flex;gap:8px}
.cbtn{flex:1;min-height:38px;background:var(--g2);border:1px solid var(--ln);color:#fff;border-radius:10px;font-family:var(--fr);font-size:14px;font-weight:700;transition:border-color .2s,box-shadow .2s,background .2s}
.cbtn:hover{border-color:var(--red);box-shadow:0 0 16px var(--rg)}.cbtn.del:hover{background:rgba(255,26,26,.18)}
.empty{grid-column:1/-1;text-align:center;color:var(--tx2);padding:48px 20px;border:1px dashed rgba(255,26,26,.35);border-radius:18px;font-family:var(--fr);font-size:17px}
.sk-card{height:206px;border-radius:18px;border:1px solid var(--ln);background:linear-gradient(100deg,#0d0d0d 30%,#1c1c1c 50%,#0d0d0d 70%);background-size:200% 100%;animation:shim 1.4s linear infinite}
#skel{display:none;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}
.sk #skel{display:grid}
.sk .stat-num,.sk .exp-hero-num span{color:transparent;border-radius:8px;background:linear-gradient(100deg,#151515 30%,#2a2a2a 50%,#151515 70%);background-size:200% 100%;animation:shim 1.2s linear infinite}
.log-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.log-clear{min-height:44px;padding:0 6px;font-family:var(--fr);font-size:15px;font-weight:700;color:var(--mut);background:none;border:0;transition:color .2s}.log-clear:hover{color:var(--red)}
.log-box{border-radius:16px;padding:12px 14px;max-height:260px;overflow-y:auto;display:flex;flex-direction:column;gap:6px;-webkit-mask-image:linear-gradient(#000 85%,transparent);mask-image:linear-gradient(#000 85%,transparent)}
.log-entry{display:flex;gap:12px;font-size:13px;line-height:1.45}
.log-entry:first-child{animation:ent .9s ease-out}
@keyframes ent{from{background:rgba(255,26,26,.28);translate:0 -6px}to{background:transparent;translate:0 0}}
.log-ts{color:var(--red);opacity:.8;flex:0 0 auto;font-size:12px}
.log-msg{word-break:break-word;color:var(--tx2)}.l-success{color:var(--ok)}.l-warning{color:var(--amb)}.l-error{color:#ff5a5a}.l-info{color:#fff}
.overlay{position:fixed;inset:0;z-index:200;display:none;place-items:center;padding:18px;background:rgba(0,0,0,.78);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.overlay.open{display:grid}.overlay.open .modal{animation:up .4s var(--e)}
.modal{width:min(440px,100%);max-height:100%;overflow-y:auto;border-radius:22px;padding:24px;border-color:rgba(255,26,26,.5);box-shadow:0 0 60px rgba(255,26,26,.22),0 30px 90px #000}
.modal h2{font-family:var(--fd);font-weight:900;font-style:italic;font-size:22px;margin-bottom:6px}
.modal p{font-size:13.5px;color:var(--tx2);margin-bottom:16px}
.tabs{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;background:#000;border:1px solid var(--ln);border-radius:14px;margin-bottom:16px}
.tab{min-height:44px;border:0;border-radius:10px;background:transparent;color:var(--tx2);font-family:var(--fr);font-size:15px;font-weight:700;transition:background .2s}
.tab.active{background:var(--red);color:#fff;box-shadow:0 0 18px var(--rg)}
.field{margin-bottom:14px}.field label{display:block;font-size:13px;color:var(--tx2);margin-bottom:6px}
.field .inp{width:100%;height:48px}
.pane{display:none}.pane.active{display:block}
.modal-foot{display:flex;gap:10px;margin-top:8px}.modal-foot button{flex:1;height:48px}
.toasts{position:fixed;right:20px;bottom:20px;z-index:300;display:flex;flex-direction:column;gap:10px;pointer-events:none}
.toast{max-width:360px;padding:12px 16px;font-size:14px;font-weight:500;background:rgba(10,10,10,.92);backdrop-filter:blur(12px);border:1px solid rgba(255,26,26,.35);border-left:4px solid var(--ok);border-radius:12px;box-shadow:0 12px 40px #000,0 0 24px rgba(255,26,26,.15);animation:tin .4s var(--e),tout .4s ease-in 3s forwards}
.toast.err{border-left-color:var(--red)}
@keyframes tin{from{opacity:0;translate:40px 0}}@keyframes tout{to{opacity:0;translate:40px 0}}
.bnav{display:none}

.role-user .ctrl-stack,.role-user .ctrl-toggle,.role-user .card-btns,.role-user .log-clear,.role-user .divider,.role-user [data-go=ctrl]{display:none!important}
.role-user button.badge.mode{pointer-events:none;cursor:default}

@media(min-width:901px){
.sidebar .log-sec{flex:none;display:flex;flex-direction:column}
.sidebar .log-box{flex:none;height:360px;max-height:360px;padding:10px}
.sidebar .log-entry{flex-direction:column;gap:0}
}
@media(max-width:900px){
.app{display:flex;flex-direction:column;height:auto;min-height:100dvh;padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}
.header{position:sticky;top:0;padding:0 14px;height:62px;flex:0 0 auto}
.sidebar{border-right:0;overflow:visible;background:none;padding:14px}
.stat-grid{grid-template-columns:repeat(2,1fr)}
.ctrl-toggle{display:flex;width:100%;min-height:48px;align-items:center;justify-content:center;background:var(--g2);border:1px solid rgba(255,26,26,.3);border-radius:12px;font-family:var(--fr);font-size:16px;font-weight:700}
.ctrl-stack{display:none}.ctrl-stack.open{display:flex}
.main{overflow:visible;padding:6px 14px 20px}
.brand-sub,.rolechip{display:none}
.toasts{left:14px;right:14px;bottom:calc(88px + env(safe-area-inset-bottom,0px))}.toast{max-width:none}
.bnav{display:grid;grid-template-columns:repeat(5,1fr);align-items:center;position:fixed;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));height:64px;z-index:150;padding:0 6px;border-radius:22px;background:rgba(8,8,8,.88);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border:1px solid rgba(255,26,26,.4);box-shadow:0 10px 40px #000,0 0 30px rgba(255,26,26,.18)}
.bnav button{min-height:52px;background:none;border:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;color:var(--mut);font-family:var(--fr);font-size:12.5px;font-weight:700;border-radius:14px;transition:color .2s}
.bnav button svg{width:22px;height:22px}.bnav button.on{color:var(--red)}.bnav button.on svg{filter:drop-shadow(0 0 6px var(--red))}
.bnav .fab{width:58px;height:58px;min-height:58px;margin:-24px auto 0;border-radius:50%;background:linear-gradient(135deg,#d90000,var(--red));color:#fff;box-shadow:0 0 28px var(--rg);border:3px solid #000}
}
@media(max-width:520px){
.accounts-grid,#skel{grid-template-columns:1fr}.search{width:100%;flex:1 1 100%}
.header{padding:0 10px}.brand-name{font-size:15px}.logo{width:40px;height:40px}
.btn-primary{padding:0;width:44px}.btn-primary .lbl{display:none}
.live span{display:none}.header-right{gap:8px}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}

/* ================= 2026 THEME LAYER (red + cyan) ================= */
:root{--cy:#00d9ff;--cyg:rgba(0,217,255,.35);--fm:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace}
body{background-image:radial-gradient(55% 38% at 50% -8%,rgba(255,26,26,.22),transparent 70%),radial-gradient(38% 30% at 0% 100%,rgba(0,217,255,.11),transparent 70%),radial-gradient(40% 30% at 100% 100%,rgba(255,26,26,.10),transparent 70%)}
body::after{content:'';position:fixed;right:-180px;top:22%;width:520px;height:520px;border-radius:50%;pointer-events:none;background:radial-gradient(circle,rgba(0,217,255,.10),transparent 65%);filter:blur(30px);animation:aur 16s ease-in-out infinite alternate}
@keyframes aur{to{translate:-90px 70px;scale:1.2}}
.header{border-bottom:0;box-shadow:0 1px 40px rgba(255,26,26,.10)}
@media(min-width:901px){.header{position:relative}}
.header::after{content:'';position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,var(--red) 25%,var(--cy) 75%,transparent);opacity:.75}
.header{position:relative}
@media(max-width:900px){.header{position:sticky}}
.logo::before{background:conic-gradient(var(--red),transparent 35%,var(--cy) 55%,transparent 72%,var(--red))}
.brand-name{background:linear-gradient(100deg,#fff 35%,#9ff1ff);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 14px rgba(255,26,26,.5))}
.brand-sub{letter-spacing:.14em;text-transform:uppercase;font-size:12px;color:var(--cy);opacity:.8}
.rolechip{border-color:rgba(0,217,255,.45);color:var(--cy);background:rgba(0,217,255,.08);letter-spacing:.08em;text-transform:uppercase}
.live{padding:6px 12px;border-radius:99px;border:1px solid rgba(43,255,136,.35);background:rgba(43,255,136,.07)}
.live.off{border-color:rgba(255,26,26,.45);background:rgba(255,26,26,.08)}
.btn-primary{position:relative;overflow:hidden;background:linear-gradient(100deg,#c40000,var(--red) 55%,#ff5a3c)}
.btn-primary::after{content:'';position:absolute;top:0;bottom:0;width:60px;left:-80px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);transform:skewX(-20deg);transition:left .55s}
.btn-primary:hover::after{left:120%}
.btn-icon:hover{border-color:var(--cy);box-shadow:0 0 20px var(--cyg);color:var(--cy)}
.glass,.exp-hero,.stat-card,.row-between,.mode-row,.log-box,.acard,.modal{border-color:rgba(255,255,255,.09);box-shadow:0 10px 40px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.05)}
.slabel{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.exp-hero{background:linear-gradient(160deg,rgba(255,26,26,.12),rgba(0,217,255,.05) 60%,rgba(255,255,255,.01))}
.exp-hero::after{background:linear-gradient(90deg,transparent,var(--red),var(--cy),transparent);box-shadow:0 0 18px var(--cyg)}
.exp-hero-num span{background:linear-gradient(100deg,#fff 30%,#a6f3ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.sk .exp-hero-num span{-webkit-background-clip:border-box;background-clip:border-box}
.exp-hero-num small{color:var(--cy)}
.exp-hero-sub{font-family:var(--fm);font-size:13px}
.stat-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(var(--red),var(--cy));opacity:.8}
.stat-card:hover{border-color:rgba(0,217,255,.5);box-shadow:0 0 28px rgba(0,217,255,.16)}
.stat-num{font-family:var(--fm);font-weight:600;font-size:27px;letter-spacing:-.02em}
.c-green{color:var(--ok)}.c-amber{color:var(--amb)}.c-fire{color:#fff}
.stat-lbl{letter-spacing:.06em;text-transform:uppercase;font-size:11.5px}
.inp:focus{border-color:var(--cy);box-shadow:0 0 0 3px rgba(0,217,255,.12),0 0 22px rgba(0,217,255,.15)}
.btn-ghost:hover,.btn-block:hover{border-color:rgba(0,217,255,.55)}
.mbtn.active{background:linear-gradient(100deg,#c40000,var(--red))}
.sec-title::after{content:'';display:block;width:46px;height:2px;margin-top:7px;border-radius:2px;background:linear-gradient(90deg,var(--red),var(--cy));box-shadow:0 0 12px var(--cyg)}
.sec-title small{font-family:var(--fm);font-size:13px;color:var(--cy)}
.acard::before{height:3px;background:linear-gradient(90deg,var(--c,var(--red)),var(--cy) 65%,transparent)}
.acard:hover{border-color:rgba(0,217,255,.45);box-shadow:0 0 34px rgba(0,217,255,.14),0 14px 40px rgba(0,0,0,.6)}
.acard::after{background:radial-gradient(260px circle at var(--mx) var(--my),rgba(0,217,255,.13),transparent 60%)}
.st-match:hover{border-color:rgba(255,26,26,.8)}
.avatar{border:1px solid transparent;background:linear-gradient(#000,#000) padding-box,linear-gradient(135deg,var(--red),var(--cy)) border-box;box-shadow:inset 0 0 16px rgba(255,26,26,.18),0 0 18px rgba(0,217,255,.12)}
.lvl-tag{color:var(--cy)}
.uid{font-family:var(--fm);font-size:12px;letter-spacing:.02em}
.nick{letter-spacing:.01em}
.exp-val{font-family:var(--fm);font-size:23px;font-weight:600;text-shadow:0 0 16px var(--cyg)}
.exp-need,.exp-lbl{font-family:var(--fm);font-size:11.5px}
.ring-fill{filter:drop-shadow(0 0 5px var(--cy))}
.ring-pct{font-family:var(--fm);font-size:12.5px}
.limit i{background:linear-gradient(90deg,#8a0000,var(--red),var(--cy),var(--red));background-size:200% 100%}
.meta{font-size:12.5px}.meta b{font-family:var(--fm);font-weight:500}
.cbtn:hover{border-color:rgba(0,217,255,.55);box-shadow:0 0 16px var(--cyg)}.cbtn.del:hover{border-color:var(--red);box-shadow:0 0 16px var(--rg)}
.badge{letter-spacing:.04em}
.log-entry{font-family:var(--fm);font-size:12px}.log-ts{color:var(--cy);font-size:11px}
.toast{border-left-color:var(--cy)}.toast.err{border-left-color:var(--red)}
.bnav button.on{color:var(--cy)}.bnav button.on svg{filter:drop-shadow(0 0 6px var(--cy))}
.bnav{border-color:rgba(0,217,255,.28)}
.empty{border-color:rgba(0,217,255,.3)}
@media(max-width:520px){.hide-sm{display:none!important}}

/* ---------- JSON database modal ---------- */
.role-user #jsonBtn,.role-user #jsonOpen{display:none!important}
.jm{width:min(480px,100%)}
.jm h2{display:flex;align-items:center;gap:10px}
.jm-stats{display:grid;grid-template-columns:1.15fr 1fr 1.35fr;gap:8px;margin-bottom:12px}
.jm-stats>div{padding:10px 12px;border-radius:12px;background:rgba(0,0,0,.45);border:1px solid var(--ln);min-width:0}
.jm-stats b{display:block;font-family:var(--fm);font-weight:600;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.jm-stats>div:first-child b{color:var(--cy)}
.jm-stats span{display:block;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);margin-top:3px}
.jm-note{font-size:12.5px;color:var(--amb);margin:-2px 0 12px}
.dz{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;padding:20px 14px;margin-bottom:12px;border-radius:16px;cursor:pointer;border:1.5px dashed rgba(0,217,255,.4);background:rgba(0,217,255,.04);transition:background .2s,border-color .2s,box-shadow .2s}
.dz:hover,.dz.drag,.dz:focus-visible{background:rgba(0,217,255,.1);border-color:var(--cy);box-shadow:0 0 28px rgba(0,217,255,.18)}
.dz svg{width:30px;height:30px;color:var(--cy);margin-bottom:4px}
.dz b{font-family:var(--fr);font-size:16px;word-break:break-all}
.dz span{font-size:12.5px;color:var(--mut)}
.dz.ready{border-style:solid;border-color:rgba(43,255,136,.5);background:rgba(43,255,136,.06)}
.dz.ready svg{color:var(--ok)}
.dz.bad{border-color:var(--red);background:rgba(255,26,26,.07)}.dz.bad svg{color:var(--red)}
.seg{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;margin-bottom:6px;background:#000;border:1px solid var(--ln);border-radius:14px}
.seg button{min-height:42px;border:0;border-radius:10px;background:transparent;color:var(--tx2);font-family:var(--fr);font-size:15px;font-weight:700;transition:background .2s}
.seg button.on{background:linear-gradient(100deg,#0098b8,var(--cy));color:#001418;box-shadow:0 0 18px var(--cyg)}
.seg-hint{font-size:12.5px;color:var(--mut);min-height:2.4em;margin-bottom:6px}
.jm-bar{height:5px;border-radius:99px;background:#1a1a1a;overflow:hidden;margin:4px 0 8px}
.jm-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--red),var(--cy));transition:width .2s}
#jmMsg{min-height:1.3em;margin:0 0 10px}
#jmMsg.ok{color:var(--ok)}#jmMsg.er{color:#ff7a7a}
.jm-up{width:100%}
.jm-danger{margin-top:18px;padding:14px;border-radius:14px;border:1px solid rgba(255,26,26,.35);background:rgba(255,26,26,.06)}
.jm-dt{font-family:var(--fr);font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:12.5px;color:var(--red);margin-bottom:8px}
.jm-chk{display:flex;gap:10px;align-items:flex-start;margin-bottom:10px;cursor:pointer;font-size:12.5px;color:var(--tx2);line-height:1.4}
.jm-chk input{margin-top:2px;width:18px;height:18px;accent-color:var(--red);flex:0 0 auto}
.jm-del{background:rgba(255,26,26,.14);border-color:rgba(255,26,26,.55)}
.jm-del:disabled{opacity:.4;cursor:not-allowed}
.jm .modal-foot{margin-top:16px}
.jm-dl{display:flex;align-items:center;justify-content:center;flex:1;height:48px;text-decoration:none}
</style>
</head>
<body class="sk">
<svg width="0" height="0" style="position:absolute;pointer-events:none"><defs><linearGradient id="expGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#ff1a1a"/><stop offset="100%" stop-color="#00d9ff"/></linearGradient></defs></svg>
<div class="app">
<header class="header stg">
  <div class="brand">
    <div class="logo"><img src="/logo.jpg" alt="ARAFAT FLEX" width="46" height="46"></div>
    <div><div class="brand-name">ARAFAT FLEX</div><div class="brand-sub">Level Up control room</div></div>
  </div>
  <div class="header-right">
    <span class="rolechip" id="roleChip"></span>
    <div class="live" id="live"><i></i><span id="liveTxt">Live</span></div>
    <button class="btn-icon hide-sm" id="jsonBtn" type="button" title="Accounts database (accounts.json)" aria-label="Accounts database"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg></button>
    <button class="btn-icon" id="logoutBtn" type="button" title="Logout" aria-label="Logout"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/></svg></button>
    <button class="btn-primary" id="openAdd" type="button" aria-label="Add account"><svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 2a.5.5 0 01.5.5v5h5a.5.5 0 010 1h-5v5a.5.5 0 01-1 0v-5h-5a.5.5 0 010-1h5v-5A.5.5 0 018 2z"/></svg><span class="lbl">Add Account</span></button>
  </div>
</header>

<aside class="sidebar" id="sideTop">
  <div class="stg" style="--i:1">
    <div class="slabel">Total EXP farmed</div>
    <div class="exp-hero"><div class="exp-hero-num"><small>EXP</small><span id="totalExp">0</span></div><div class="exp-hero-sub" id="totalSub">0 matches</div></div>
  </div>
  <div class="stg" style="--i:2">
    <div class="slabel">Accounts</div>
    <div class="stat-grid">
      <div class="stat-card wide"><div class="stat-num c-fire" id="sTotal">0</div><div class="stat-lbl">Total</div></div>
      <div class="stat-card"><div class="stat-num c-green" id="sOnline">0</div><div class="stat-lbl">Online</div></div>
      <div class="stat-card"><div class="stat-num c-amber" id="sConn">0</div><div class="stat-lbl">Connecting</div></div>
      <div class="stat-card"><div class="stat-num c-red" id="sOffline">0</div><div class="stat-lbl">Offline</div></div>
      <div class="stat-card"><div class="stat-num c-muted" id="sPaused">0</div><div class="stat-lbl">Paused</div></div>
    </div>
  </div>
  <button class="ctrl-toggle" id="ctrlToggle" type="button">⚙ Controls ▾</button>
  <div class="divider"></div>
  <div class="ctrl-stack stg" style="--i:3" id="ctrlStack">
    <div class="slabel" style="margin-bottom:-6px">Controls</div>
    <div class="row-between"><span class="row-label">All bots</span><label class="tgl"><input type="checkbox" id="globalToggle" checked aria-label="All bots"><span class="tgl-track"></span></label></div>
    <div>
      <div class="slabel">Match mode — all accounts</div>
      <div class="mode-row">
        <button class="mbtn mbtn-br" id="m-BR" type="button">⚔ BR</button>
        <button class="mbtn mbtn-lw" id="m-LONE_WOLF" type="button">🐺 LW</button>
        <button class="mbtn mbtn-auto" id="m-AUTO" type="button">🔄 Auto</button>
      </div>
    </div>
    <div>
      <div class="slabel">EXP limit (auto-delete)</div>
      <div class="input-row"><input class="inp" type="text" inputmode="numeric" id="limitInp" placeholder="0 = no limit"><button class="btn-ghost" id="limitBtn" type="button">Set</button></div>
      <div class="hint" id="limitHint"></div>
    </div>
    <div>
      <div class="slabel">Level limit (auto-delete)</div>
      <div class="input-row"><input class="inp" type="text" inputmode="numeric" id="levelInp" placeholder="0 = no limit"><button class="btn-ghost" id="levelBtn" type="button">Set</button></div>
      <div class="hint" id="levelHint"></div>
    </div>
    <div>
      <div class="slabel">User ID limit (per user)</div>
      <div class="input-row"><input class="inp" type="text" inputmode="numeric" id="userLimitInp" placeholder="0 = no limit"><button class="btn-ghost" id="userLimitBtn" type="button">Set</button></div>
      <div class="hint" id="userLimitHint"></div>
    </div>
    <button class="btn-block" id="reloadBtn" type="button">↺ Reload accounts.json</button>
    <button class="btn-block" id="jsonOpen" type="button">🗄 Upload / Delete accounts.json</button>
  </div>
</aside>

<main class="main">
  <section id="accSec" class="stg" style="--i:2">
    <div class="sec-head">
      <div class="sec-title">Accounts<small id="countTxt"></small></div>
      <input class="inp search" id="search" type="search" placeholder="Search name or UID…" autocomplete="off">
    </div>
    <div id="skel"><div class="sk-card"></div><div class="sk-card"></div><div class="sk-card"></div></div>
    <div class="accounts-grid" id="grid"></div>
  </section>
  <section class="log-sec stg" style="--i:3" id="logSec">
    <div class="log-head"><div class="sec-title">Activity log</div><button class="log-clear" id="logClear" type="button">Clear</button></div>
    <div class="log-box" id="logBox"></div>
  </section>
</main>
</div>

<nav class="bnav" aria-label="Sections">
  <button type="button" data-go="stats" class="on"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/></svg>Stats</button>
  <button type="button" data-go="acc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>Accounts</button>
  <button type="button" data-go="add" class="fab" aria-label="Add account"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button>
  <button type="button" data-go="log"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg>Logs</button>
  <button type="button" data-go="ctrl"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>Controls</button>
</nav>

<div class="overlay" id="overlay">
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="mTitle">
    <h2 id="mTitle">Add account</h2><p>Connect a Free Fire account. It is validated before the bot starts.</p>
    <div class="tabs"><button class="tab active" data-tab="guest" type="button">Guest Account</button><button class="tab" data-tab="token" type="button">Access Token</button></div>
    <div class="pane active" data-pane="guest">
      <div class="field"><label for="fUid">UID</label><input class="inp" id="fUid" inputmode="numeric" autocomplete="off" placeholder="Player UID"></div>
      <div class="field"><label for="fPwd">Password</label><input class="inp" id="fPwd" type="password" autocomplete="off" placeholder="Account password"></div>
    </div>
    <div class="pane" data-pane="token">
      <div class="field"><label for="fTok">Access Token</label><input class="inp" id="fTok" autocomplete="off" placeholder="Paste access token"></div>
    </div>
    <div class="field"><label for="fReg">Server Region</label>
      <select class="inp" id="fReg"><option value="BD">Bangladesh</option><option value="IND">India</option><option value="SG">Singapore</option><option value="ID">Indonesia</option><option value="BR">Brazil</option><option value="US">United States</option></select></div>
    <div class="modal-foot"><button class="btn-ghost" id="addCancel" type="button">Cancel</button><button class="btn-primary" id="addSubmit" type="button">Validate &amp; Start</button></div>
  </div>
</div>
<div class="overlay" id="jsonOverlay">
  <div class="modal jm" role="dialog" aria-modal="true" aria-labelledby="jmTitle">
    <h2 id="jmTitle">Accounts database</h2>
    <p>Upload a new <b>accounts.json</b> or clear the current one. A backup is saved automatically before every change.</p>
    <div class="jm-stats">
      <div><b id="jmCount">–</b><span>Accounts</span></div>
      <div><b id="jmSize">–</b><span>Size</span></div>
      <div><b id="jmDate">–</b><span>Updated</span></div>
    </div>
    <div class="jm-note" id="jmMulti" hidden></div>
    <label class="dz" id="jmDrop" tabindex="0">
      <input type="file" id="jmFile" accept=".json,application/json" hidden>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 17v-6"/><path d="m9.5 13.5 2.5-2.5 2.5 2.5"/></svg>
      <b id="jmDzTitle">Drop accounts.json here</b><span id="jmDzSub">or tap to choose a file</span>
    </label>
    <div class="seg" id="jmMode"><button type="button" class="on" data-m="replace">Replace all</button><button type="button" data-m="merge">Merge</button></div>
    <div class="seg-hint" id="jmModeHint">Replace: the file becomes the new database. Accounts missing from it are stopped.</div>
    <div class="jm-bar" id="jmBarWrap" hidden><i id="jmBar"></i></div>
    <div class="hint" id="jmMsg"></div>
    <button class="btn-primary jm-up" id="jmUpload" type="button" disabled>Upload &amp; apply</button>
    <div class="jm-danger">
      <div class="jm-dt">Danger zone</div>
      <label class="jm-chk"><input type="checkbox" id="jmSure"><span>I understand this clears every account in accounts.json and stops their bots.</span></label>
      <button class="btn-block jm-del" id="jmDelete" type="button" disabled>🗑 Delete all accounts</button>
    </div>
    <div class="modal-foot"><a class="btn-ghost jm-dl" href="/api/json/download" download="accounts.json">⬇ Download</a><button class="btn-ghost" id="jmClose" type="button">Close</button></div>
  </div>
</div>
<div class="toasts" id="toasts" aria-live="polite"></div>

<script>
const EXP_LIST=[0,48,202,544,1012,1844,2792,3800,4870,6004,7192,8448,9760,11140,12566,14060,15610,17224,18902,20632,22424,24278,26192,28166,30200,32294,34448,37804,41274,44870,48582,53394,58566,64096,69994,76260,83506,91128,99322,108092,120144,133266,147472,162760,179126,196572,215368,235316,257010,279860,304056,348318,394982,444044,495508,549364,633756,721744,813336,908522,1041438,1180352,1325266,1476184,1634300,1840946,2056594,2281242,2514880,2757530,3059506,3372284,3699456,4041030,4397002,4829104,5282204,5756304,6251404,6767502,7381324,8043154,8752982,9510808,10316638,11277190,12291748,13360304,14482858,15659418,17026708,18453990,19941280,21488570,23095858,24763138,26490428,28277708,30124996,32032284];
// EXP_LIST[i] = total EXP needed to reach level i+1
const $=id=>document.getElementById(id);
const esc=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=v=>{const n=Number(v);return Number.isFinite(n)?n.toLocaleString():'0'};
const num=v=>{const n=Number(v);return Number.isFinite(n)?n:0};
let globalRunning=true,modeChoice=null,limitLoaded=false,limitBusy=false,toggleBusy=false,lastLogSig='',lastData=null,tab='guest';
const cards=new Map();
let levelLoaded=false,levelBusy=false,userLimitLoaded=false,userLimitBusy=false;

function toast(msg,err){const t=document.createElement('div');t.className='toast'+(err?' err':'');t.textContent=msg;$('toasts').appendChild(t);setTimeout(()=>t.remove(),3400)}
async function api(path,body){
  const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{})});
  if(r.status===401){location.href='/login';throw new Error('Session expired')}
  const d=await r.json().catch(()=>({}));
  if(!r.ok||d.status==='error'||d.success===false)throw new Error(d.error||d.message||'Request failed');
  return d;
}

function status(s){
  const v=String(s||'ONLINE').toUpperCase().replace(/ +/g,'_');
  if(v==='CONNECTING')return{k:'connecting',l:'◌ Connecting',g:'conn'};
  if(v==='SEARCHING'||v==='SEARCH')return{k:'connecting',l:'◌ Searching',g:'on'};
  if(v==='IN_MATCH'||v==='MATCH'||v==='PLAYING')return{k:'match',l:'▶ In Match',g:'on'};
  if(v==='OFFLINE'||v==='DISCONNECTED')return{k:'offline',l:'● Offline',g:'off'};
  if(v==='ERROR'||v==='FAILED')return{k:'offline',l:'● Error',g:'off'};
  if(v==='PAUSED'||v==='STOPPED')return{k:'paused',l:'⏸ Paused',g:'pause'};
  return{k:'online',l:'● Online',g:'on'};
}
function progress(level,exp){
  const lv=Math.max(1,Math.floor(num(level))),cur=EXP_LIST[lv-1],nxt=EXP_LIST[lv];
  if(cur===undefined)return{pct:0,need:0,max:true};
  if(nxt===undefined)return{pct:100,need:0,max:true};
  const pct=Math.min(100,Math.max(0,(num(exp)-cur)/(nxt-cur)*100));
  return{pct,need:Math.max(0,nxt-num(exp)),max:false};
}
function ringSvg(){const r=23.75,c=2*Math.PI*r;return`<svg class="ring-svg" width="54" height="54" viewBox="0 0 54 54"><circle class="ring-bg" cx="27" cy="27" r="${r}"/><circle class="ring-fill" cx="27" cy="27" r="${r}" stroke-dasharray="${c.toFixed(2)}" stroke-dashoffset="${c.toFixed(2)}"/></svg><div class="ring-pct">0%</div>`}

function cardHtml(){return`<div class="card-top"><div class="avatar"><span class="lvl"></span></div><div class="card-info"><div class="nick"></div><div class="uid"></div><div class="badge-row"><span class="badge st"></span><button type="button" class="badge mode" title="Click to switch BR / Lone Wolf"></button><span class="badge b-reg reg"></span></div></div></div>
<div class="exp-row"><div class="ring-wrap">${ringSvg()}</div><div><div class="exp-lbl">EXP this session</div><div class="exp-val"></div><div class="exp-need"></div></div></div>
<div class="limit" hidden><i></i></div>
<div class="meta"></div>
<div class="note err" hidden></div><div class="note info" hidden></div>
<div class="card-btns"><button type="button" class="cbtn ref">↻ Refresh</button><button type="button" class="cbtn del">🗑 Delete</button></div>`}

function makeCard(uid){
  const el=document.createElement('article');
  el.dataset.uid=uid;el.innerHTML=cardHtml();
  el.querySelector('.mode').addEventListener('click',()=>{const a=el._acc;if(a)setMatchType(uid,a.match_type==='BR'?'LONE_WOLF':'BR')});
  el.querySelector('.ref').addEventListener('click',()=>refreshAcc(uid));
  el.querySelector('.del').addEventListener('click',()=>deleteAcc(uid));
  return el;
}
function setText(el,t){if(el.textContent!==t)el.textContent=t}
function updateCard(el,a,limit){
  el._acc=a;
  const st=status(a.status),nick=a.nickname||a.name||'Unknown',uid=String(a.uid),lv=num(a.level)||1;
  const cur=num(a.current_exp??a.exp),gained=a.gained_exp!=null?num(a.gained_exp):Math.max(0,cur-num(a.initial_exp));
  const p=progress(lv,cur),mt=a.match_type==='BR'?'BR':'LONE_WOLF',region=a.region||'—';
  el.className='acard st-'+st.k;
  el.querySelector('.lvl').innerHTML=String(lv)+'<span class="lvl-tag">LV</span>';
  setText(el.querySelector('.nick'),nick);el.querySelector('.nick').title=nick;
  setText(el.querySelector('.uid'),'#'+uid);
  const s=el.querySelector('.st');setText(s,st.l);s.className='badge st b-'+st.k;
  const m=el.querySelector('.mode');setText(m,mt==='BR'?'⚔ BR':'🐺 LW');m.className='badge mode '+(mt==='BR'?'b-br':'b-lw');
  setText(el.querySelector('.reg'),region);
  const circ=2*Math.PI*23.75;
  el.querySelector('.ring-fill').style.strokeDashoffset=(circ-p.pct/100*circ).toFixed(2);
  setText(el.querySelector('.ring-pct'),Math.round(p.pct)+'%');
  setText(el.querySelector('.exp-val'),'+'+fmt(gained));
  setText(el.querySelector('.exp-need'),p.max?'Max level':fmt(p.need)+' to Lv'+(lv+1));
  const lim=el.querySelector('.limit');
  if(limit>0){lim.hidden=false;lim.firstElementChild.style.width=Math.min(100,gained/limit*100)+'%';lim.title='Limit: '+fmt(gained)+' / '+fmt(limit)}else lim.hidden=true;
  const lm=a.last_match_time||'No match yet';
  el.querySelector('.meta').innerHTML='<b>'+fmt(a.matches_played??a.matches)+'</b> matches · Region: '+esc(region)+'<br>EXP '+fmt(num(a.initial_exp))+' → <b>'+fmt(cur)+'</b> · Last match: '+esc(lm);
  const er=el.querySelector('.note.err'),inf=el.querySelector('.note.info');
  er.hidden=!a.last_error;if(a.last_error)setText(er,a.last_error);
  inf.hidden=!a.last_info;if(a.last_info)setText(inf,a.last_info);
  el._search=(nick+' '+uid).toLowerCase();
}

function render(data){
  const accs=Array.isArray(data.accounts)?data.accounts.slice():[];
  // Highest level first; same level → UID order (EXP বদলালে কার্ড জায়গা বদলাবে না)
  accs.sort((a,b)=>num(b.level)-num(a.level)||String(a.uid).localeCompare(String(b.uid)));
  const limit=num(data.exp_limit),grid=$('grid'),q=$('search').value.trim().toLowerCase();
  const seen=new Set();let g={on:0,conn:0,off:0,pause:0};
  accs.forEach((a,i)=>{
    const uid=String(a.uid);seen.add(uid);
    let el=cards.get(uid);if(!el){el=makeCard(uid);cards.set(uid,el)}
    updateCard(el,a,limit);
    g[status(a.status).g]++;
    el.hidden=!!q&&!el._search.includes(q);
    if(grid.children[i]!==el)grid.insertBefore(el,grid.children[i]||null);   // keeps level order, moves only what changed
  });
  cards.forEach((el,uid)=>{if(!seen.has(uid)){el.remove();cards.delete(uid)}});
  let emp=grid.querySelector('.empty');
  if(!accs.length){if(!emp){emp=document.createElement('div');emp.className='empty';emp.textContent='No bots connected. Add a Free Fire account to start.';grid.appendChild(emp)}}else if(emp)emp.remove();
  const shown=q?accs.filter(a=>(String(a.nickname||'')+' '+a.uid).toLowerCase().includes(q)).length:accs.length;
  $('countTxt').textContent=q?shown+' / '+accs.length:accs.length+' total';
  $('totalExp').textContent=fmt(data.total_gained_exp);
  const up=num(data.uptime),h=Math.floor(up/3600),mi=Math.floor(up%3600/60);
  $('totalSub').textContent=fmt(data.total_matches)+' matches · uptime '+(h?h+'h ':'')+mi+'m';
  $('sTotal').textContent=fmt(accs.length);$('sOnline').textContent=fmt(g.on);$('sConn').textContent=fmt(g.conn);$('sOffline').textContent=fmt(g.off);$('sPaused').textContent=fmt(g.pause);
  // global toggle
  if(!toggleBusy&&data.global_running!==undefined){globalRunning=!!data.global_running;$('globalToggle').checked=globalRunning}
  // exp limit
  $('limitHint').textContent=limit>0?'Auto-delete at +'+fmt(limit)+' EXP':'No limit (accounts are never auto-deleted)';
  if(!limitLoaded&&data.exp_limit!==undefined&&!limitBusy){$('limitInp').value=data.exp_limit;limitLoaded=true}
  // role (Admin / User)
  const isUser=data.role==='user';document.body.classList.toggle('role-user',isUser);$('roleChip').textContent=isUser?'User':'Admin';
  // level limit
  const ll=num(data.level_limit);
  $('levelHint').textContent=ll>0?'Auto-delete at Lv'+ll:'No level limit';
  if(!levelLoaded&&data.level_limit!==undefined&&!levelBusy){$('levelInp').value=data.level_limit;levelLoaded=true}
  // user add limit (admin sets how many IDs each user may add)
  const ul=num(data.user_add_limit);
  $('userLimitHint').textContent=ul>0?'Each user can add up to '+ul+' ID(s)':'No limit (users can add unlimited IDs)';
  if(!userLimitLoaded&&data.user_add_limit!==undefined&&!userLimitBusy){$('userLimitInp').value=data.user_add_limit;userLimitLoaded=true}
  // mode highlight
  const mts=accs.map(a=>a.match_type==='BR'?'BR':'LONE_WOLF');
  let act=modeChoice;
  if(act!=='AUTO'&&mts.length){act=mts.every(x=>x==='BR')?'BR':mts.every(x=>x==='LONE_WOLF')?'LONE_WOLF':null}
  ['BR','LONE_WOLF','AUTO'].forEach(k=>$('m-'+k).classList.toggle('active',act===k));
  renderLogs(data.logs);
}

function renderLogs(logs){
  logs=Array.isArray(logs)?logs:[];
  const last=logs[logs.length-1],sig=logs.length+'|'+(last?last.time+last.message:'');
  if(sig===lastLogSig)return;lastLogSig=sig;
  const box=$('logBox'),keepTop=box.scrollTop;
  box.innerHTML=logs.slice().reverse().map(l=>'<div class="log-entry"><span class="log-ts">'+esc(l.time)+'</span><span class="log-msg l-'+esc(l.level||'info')+'">'+esc(l.message)+'</span></div>').join('')||'<div class="log-entry"><span class="log-ts">—</span><span class="log-msg">No activity yet</span></div>';
  box.scrollTop=keepTop;   // রিফ্রেশে স্ক্রল উপরে লাফিয়ে যাবে না
}

async function fetchStats(){
  try{
    const r=await fetch('/api/stats',{cache:'no-store'});
    if(r.status===401){location.href='/login';return}
    if(!r.ok)throw new Error('HTTP '+r.status);
    lastData=await r.json();render(lastData);
    $('live').className='live';$('liveTxt').textContent='Live';
  }catch(e){console.error('Stats error:',e);$('live').className='live off';$('liveTxt').textContent='Disconnected'}
}

async function setMatchType(uid,mt){
  try{await api('/api/account/match-type',{uid,match_type:mt});toast('UID '+uid+' → '+(mt==='BR'?'⚔ Battle Royale':'🐺 Lone Wolf'));modeChoice=null;await fetchStats()}
  catch(e){toast(e.message,true)}
}
async function refreshAcc(uid){try{await api('/api/account/refresh',{uid});toast('Refreshing #'+uid+'…');await fetchStats()}catch(e){toast(e.message,true)}}
async function deleteAcc(uid){
  if(!confirm('Delete account #'+uid+'?'))return;
  try{await api('/api/account/delete',{uid});toast('Account #'+uid+' deleted');await fetchStats()}catch(e){toast(e.message,true)}
}
$('globalToggle').addEventListener('change',async function(){
  const on=this.checked;toggleBusy=true;
  try{await api('/api/bot/toggle',{running:on});globalRunning=on;toast(on?'✅ সব আইডি চালু হয়েছে':'🛑 সব আইডি বন্ধ হয়েছে')}
  catch(e){this.checked=!on;toast(e.message,true)}
  toggleBusy=false;fetchStats();
});
['BR','LONE_WOLF','AUTO'].forEach(mode=>$('m-'+mode).addEventListener('click',async()=>{
  try{await api('/api/accounts/set-all-mode',{mode});modeChoice=mode;toast('✅ সব আইডি → '+(mode==='AUTO'?'🔄 Auto Level Mode':mode==='BR'?'⚔ Battle Royale':'🐺 Lone Wolf'));await fetchStats()}
  catch(e){toast(e.message,true)}
}));
async function setLimit(){
  const n=parseInt($('limitInp').value.trim().replace(/,/g,''),10);
  if(isNaN(n)||n<0){toast('❌ সঠিক সংখ্যা দিন (0 = লিমিট বন্ধ)',true);return}
  limitBusy=true;$('limitBtn').disabled=true;
  try{await api('/api/settings/exp-limit',{exp_limit:n});toast(n?'🎯 EXP লিমিট সেট: '+fmt(n):'🔓 EXP লিমিট বন্ধ');$('limitInp').value=n;limitLoaded=true;await fetchStats()}
  catch(e){toast(e.message,true)}
  limitBusy=false;$('limitBtn').disabled=false;
}
$('limitBtn').addEventListener('click',setLimit);
async function setLevelLimit(){
  const n=parseInt($('levelInp').value.trim(),10);
  if(isNaN(n)||n===1||n<0||n>200){toast('❌ লেভেল দিন 2–200 (0 = লিমিট বন্ধ)',true);return}
  levelBusy=true;$('levelBtn').disabled=true;
  try{await api('/api/settings/level-limit',{level_limit:n});toast(n?'🎚 Level লিমিট সেট: Lv'+n:'🔓 Level লিমিট বন্ধ');$('levelInp').value=n;levelLoaded=true;await fetchStats()}
  catch(e){toast(e.message,true)}
  levelBusy=false;$('levelBtn').disabled=false;
}
$('levelBtn').addEventListener('click',setLevelLimit);
async function setUserLimit(){
  const n=parseInt($('userLimitInp').value.trim(),10);
  if(isNaN(n)||n<0||n>100000){toast('❌ সঠিক সংখ্যা দিন (0 = লিমিট বন্ধ)',true);return}
  userLimitBusy=true;$('userLimitBtn').disabled=true;
  try{await api('/api/settings/user-limit',{user_add_limit:n});toast(n?'👤 প্রতি User সর্বোচ্চ '+n+'টি আইডি':'🔓 User ID লিমিট বন্ধ');$('userLimitInp').value=n;userLimitLoaded=true;await fetchStats()}
  catch(e){toast(e.message,true)}
  userLimitBusy=false;$('userLimitBtn').disabled=false;
}
$('userLimitBtn').addEventListener('click',setUserLimit);
$('userLimitInp').addEventListener('keydown',e=>{if(e.key==='Enter')setUserLimit()});
$('levelInp').addEventListener('keydown',e=>{if(e.key==='Enter')setLevelLimit()});
$('limitInp').addEventListener('keydown',e=>{if(e.key==='Enter')setLimit()});
function resetDashboard(){
  cards.forEach(el=>el.remove());cards.clear();
  const emp=$('grid').querySelector('.empty');if(emp)emp.remove();
  lastLogSig='';limitLoaded=false;levelLoaded=false;userLimitLoaded=false;modeChoice=null;lastData=null;
}
$('reloadBtn').addEventListener('click',async function(){
  const btn=this,old=btn.textContent;
  if(btn.disabled)return;
  btn.disabled=true;btn.textContent='↺ Reloading…';
  try{
    const d=await api('/api/accounts/reload');
    resetDashboard();                 // পুরনো কার্ড, লগ ও সেটিংস পরিষ্কার করে নতুন করে আঁকবে
    toast(d.message||'Accounts reloaded');
    await fetchStats();
    [1500,4000,8000].forEach(ms=>setTimeout(fetchStats,ms));   // নতুন চালু হওয়া আইডি ধরতে কয়েকবার রিফ্রেশ
  }catch(e){toast(e.message,true)}
  btn.disabled=false;btn.textContent=old;
});
$('logClear').addEventListener('click',async()=>{try{await api('/api/logs/clear');lastLogSig='';await fetchStats()}catch(e){toast(e.message,true)}});
$('search').addEventListener('input',()=>{if(lastData)render(lastData)});
$('ctrlToggle').addEventListener('click',()=>{const o=$('ctrlStack').classList.toggle('open');$('ctrlToggle').textContent='⚙ Controls '+(o?'▴':'▾')});

function openAdd(){$('overlay').classList.add('open');setTimeout(()=>{(tab==='guest'?$('fUid'):$('fTok')).focus()},50)}
function closeAdd(){$('overlay').classList.remove('open');['fUid','fPwd','fTok'].forEach(i=>$(i).value='')}
$('openAdd').addEventListener('click',openAdd);
(function(){const mq=matchMedia('(min-width:901px)');const place=()=>{const l=$('logSec');if(mq.matches)$('ctrlStack').after(l);else document.querySelector('.main').appendChild(l)};place();mq.addEventListener('change',place)})();$('addCancel').addEventListener('click',closeAdd);
$('overlay').addEventListener('click',e=>{if(e.target===$('overlay'))closeAdd()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeAdd()});
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{
  tab=b.dataset.tab;
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active',x===b));
  document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('active',p.dataset.pane===tab));
}));
$('addSubmit').addEventListener('click',async function(){
  const region=$('fReg').value,p={type:tab,region};
  if(tab==='guest'){p.uid=$('fUid').value.trim();p.password=$('fPwd').value.trim();if(!p.uid||!p.password){toast('UID এবং Password দিন',true);return}}
  else{p.token=$('fTok').value.trim();if(!p.token){toast('Access token দিন',true);return}}
  this.disabled=true;this.textContent='Validating…';
  try{await api('/api/account/add',p);toast('Account added — starting bot');closeAdd();await fetchStats()}
  catch(e){toast(e.message,true)}
  this.disabled=false;this.textContent='Validate & Start';
});

$('logoutBtn').addEventListener('click',async()=>{try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'});
fetchStats();setInterval(fetchStats,4000);
</script>

<script>
/* ARAFAT FLEX visual layer — presentation only, never touches API/logic */
(function(){
const g=id=>document.getElementById(id),rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
const num=t=>Number(String(t).replace(/[^\d.-]/g,''))||0;
/* animated counters: watch the original code's writes, then tween to the new value */
['totalExp','sTotal','sOnline','sConn','sOffline','sPaused'].forEach(id=>{
  const el=g(id);if(!el)return;let cur=0,raf=0;el._w=el.textContent;
  new MutationObserver(()=>{
    const t=el.textContent;if(t===el._w)return;
    const to=num(t),from=cur;cancelAnimationFrame(raf);
    if(rm||from===to){cur=to;el._w=t;return}
    const t0=performance.now(),d=Math.min(1100,350+Math.sqrt(Math.abs(to-from))*9);
    const step=now=>{const p=Math.min(1,(now-t0)/d),e=1-Math.pow(1-p,3);cur=Math.round(from+(to-from)*e);
      const s=p<1?cur.toLocaleString():t;el._w=s;if(el.textContent!==s)el.textContent=s;
      if(p<1)raf=requestAnimationFrame(step);else cur=to};
    raf=requestAnimationFrame(step);
  }).observe(el,{childList:true,characterData:true,subtree:true});
});
/* skeleton -> real content on first render */
const done=()=>{document.body.classList.remove('sk');const k=g('skel');if(k)k.remove()};
new MutationObserver(()=>{if(g('countTxt').textContent)done()}).observe(g('countTxt'),{childList:true,characterData:true,subtree:true});
setTimeout(done,9000);
/* staggered card entrance + 3D tilt */
const grid=g('grid');
new MutationObserver(m=>m.forEach(r=>r.addedNodes.forEach(n=>{if(n.style)n.style.animationDelay=Math.min([...grid.children].indexOf(n),10)*70+'ms'}))).observe(grid,{childList:true});
if(!rm&&matchMedia('(hover:hover) and (pointer:fine)').matches){
  let f=0;
  grid.addEventListener('pointermove',e=>{const c=e.target.closest('.acard');if(!c||f)return;
    f=requestAnimationFrame(()=>{f=0;const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
      c.style.setProperty('--ry',((x-.5)*9).toFixed(2)+'deg');c.style.setProperty('--rx',((.5-y)*9).toFixed(2)+'deg');
      c.style.setProperty('--mx',(x*100).toFixed(1)+'%');c.style.setProperty('--my',(y*100).toFixed(1)+'%')})});
  grid.addEventListener('pointerout',e=>{const c=e.target.closest('.acard');
    if(c&&!c.contains(e.relatedTarget)){c.style.setProperty('--rx','0deg');c.style.setProperty('--ry','0deg')}});
}
/* mobile bottom nav */
const T={stats:'sideTop',acc:'accSec',log:'logSec'},sm=rm?'auto':'smooth';
document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>{
  const k=b.dataset.go;
  if(k==='add'){g('openAdd').click();return}
  if(k==='ctrl'){if(!g('ctrlStack').classList.contains('open'))g('ctrlToggle').click();g('ctrlToggle').scrollIntoView({behavior:sm,block:'start'});return}
  const t=g(T[k]);if(t)t.scrollIntoView({behavior:sm,block:'start'});
}));
if('IntersectionObserver' in window){
  const btns=[...document.querySelectorAll('.bnav [data-go]')],io=new IntersectionObserver(es=>es.forEach(e=>{
    if(!e.isIntersecting)return;const k=Object.keys(T).find(x=>T[x]===e.target.id);
    btns.forEach(b=>b.classList.toggle('on',b.dataset.go===k))}),{rootMargin:'-35% 0px -55% 0px'});
  Object.values(T).forEach(id=>g(id)&&io.observe(g(id)));
}
})();
</script>
<script>
/* Accounts database manager — admin only (server enforces 403 for users) */
(function(){
const $=id=>document.getElementById(id);
const ov=$('jsonOverlay');if(!ov)return;
let file=null,mode='replace',busy=false;
const MAX=2*1024*1024;
const sz=b=>b<1024?b+' B':(b/1024).toFixed(1)+' KB';
const hints={replace:'Replace: the file becomes the new database. Accounts missing from it are stopped.',merge:'Merge: new accounts are added to the current ones. Existing accounts are kept.'};
function msg(t,k){const m=$('jmMsg');m.textContent=t||'';m.className='hint'+(k?' '+k:'')}
function dz(state,title,sub){const d=$('jmDrop');d.classList.remove('ready','bad');if(state)d.classList.add(state);$('jmDzTitle').textContent=title;$('jmDzSub').textContent=sub}
function reset(){file=null;$('jmFile').value='';dz('', 'Drop accounts.json here','or tap to choose a file');msg('');$('jmUpload').disabled=true;$('jmSure').checked=false;$('jmDelete').disabled=true;$('jmBarWrap').hidden=true;$('jmBar').style.width='0'}
async function info(){
  try{
    const d=await api('/api/json/info',{});
    $('jmCount').textContent=d.count;$('jmSize').textContent=sz(d.size||0);$('jmDate').textContent=d.modified?d.modified.slice(5):'—';
    const n=$('jmMulti');
    if(d.total_files>1){n.hidden=false;n.textContent='Also found '+(d.total_files-1)+' more accounts*.json file(s) — only accounts.json is changed here.'}else n.hidden=true;
  }catch(e){toast(e.message,true)}
}
function open(){reset();ov.classList.add('open');info()}
function close(){if(busy)return;ov.classList.remove('open')}
async function pick(f){
  file=null;$('jmUpload').disabled=true;
  if(!f)return;
  if(f.size>MAX){dz('bad',f.name,'Too large (max 2 MB)');return}
  try{
    let j=JSON.parse((await f.text()).replace(/^\uFEFF/,''));
    if(j&&!Array.isArray(j)&&Array.isArray(j.accounts))j=j.accounts;
    if(!Array.isArray(j))throw new Error('Must be a JSON list');
    const ok=j.filter(a=>a&&typeof a==='object'&&((a.uid&&a.password)||a.token)).length;
    if(!ok)throw new Error('No valid accounts found');
    if(ok!==j.length)throw new Error((j.length-ok)+' invalid entr'+(j.length-ok===1?'y':'ies'));
    file=f;dz('ready',f.name,ok+' account'+(ok===1?'':'s')+' · '+sz(f.size));msg('');$('jmUpload').disabled=false;
  }catch(e){dz('bad',f.name,e.message||'Invalid JSON')}
}
const drop=$('jmDrop');
$('jmFile').addEventListener('change',e=>pick(e.target.files[0]));
['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('drag')}));
['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('drag')}));
drop.addEventListener('drop',e=>{const f=e.dataTransfer&&e.dataTransfer.files[0];if(f)pick(f)});
drop.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();$('jmFile').click()}});
$('jmMode').addEventListener('click',e=>{const b=e.target.closest('button[data-m]');if(!b)return;mode=b.dataset.m;
  document.querySelectorAll('#jmMode button').forEach(x=>x.classList.toggle('on',x===b));$('jmModeHint').textContent=hints[mode]});
$('jmUpload').addEventListener('click',()=>{
  if(!file||busy)return;
  busy=true;$('jmUpload').disabled=true;$('jmDelete').disabled=true;$('jmBarWrap').hidden=false;msg('Uploading…');
  const fd=new FormData();fd.append('file',file);
  const x=new XMLHttpRequest();x.open('POST','/api/json/upload?mode='+mode);
  x.upload.onprogress=e=>{if(e.lengthComputable){const p=Math.round(e.loaded/e.total*100);$('jmBar').style.width=p+'%';msg('Uploading… '+p+'%')}};
  x.onload=()=>{
    busy=false;let d={};try{d=JSON.parse(x.responseText)}catch(_){}
    if(x.status===401){location.href='/login';return}
    $('jmBarWrap').hidden=true;
    if(x.status===200&&d.status==='ok'){
      toast('✓ '+(d.message||'Uploaded'));fetchStats();file=null;reset();msg((d.message||'Done')+(d.backup?' · Backup: '+d.backup:''),'ok');info();
    }else{msg('✗ '+(d.error||'Upload failed'),'er');$('jmUpload').disabled=false}
  };
  x.onerror=()=>{busy=false;$('jmBarWrap').hidden=true;msg('✗ Network error','er');$('jmUpload').disabled=false};
  x.send(fd);
});
$('jmSure').addEventListener('change',e=>{$('jmDelete').disabled=!e.target.checked||busy});
$('jmDelete').addEventListener('click',async()=>{
  if(busy||!$('jmSure').checked)return;
  busy=true;$('jmDelete').disabled=true;msg('Deleting…');
  try{
    const d=await api('/api/json/delete',{confirm:true});
    toast('✓ '+(d.message||'Deleted'));fetchStats();$('jmSure').checked=false;msg((d.message||'Done')+(d.backup?' · Backup: '+d.backup:''),'ok');info();
  }catch(e){msg('✗ '+e.message,'er');toast(e.message,true)}
  busy=false;$('jmDelete').disabled=true;
});
['jsonBtn','jsonOpen'].forEach(id=>{const b=$(id);if(b)b.addEventListener('click',open)});
$('jmClose').addEventListener('click',close);
ov.addEventListener('click',e=>{if(e.target===ov)close()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
})();
</script>
</body>
</html>
"""


# ==================== LOGIN / ACCESS KEY ====================
# Dashboard-e dhukte Access Key lagbe. Default key: ARAFAT-LEVEL
# Railway-te alada key chaile Variables-e DASHBOARD_KEY set korun (code change lagbe na).
import hmac as _hmac
import hashlib as _hashlib
import base64 as _b64

# ✅ ROLES: Admin = সব কাজ | User = শুধু দেখা + Add Account
#   Admin key  → ADMIN_KEY (না থাকলে DASHBOARD_KEY, ডিফল্ট ARAFAT-LEVEL)
#   User key   → USER_KEY  (ডিফল্ট AFX-USER)
DASHBOARD_KEY = (os.environ.get("ADMIN_KEY") or os.environ.get("DASHBOARD_KEY") or "ARAFAT-LEVEL").strip()
USER_KEY = (os.environ.get("USER_KEY") or "AFX-USER").strip()
USER_ALLOWED_PATHS = {"/", "/api/stats", "/api/account/add", "/api/logout"}
SESSION_COOKIE = "afx_session"
SESSION_DAYS = 30
_SESSION_SECRET = _hashlib.sha256(("afx-dashboard|" + DASHBOARD_KEY + "|" + USER_KEY).encode("utf-8")).digest()
_LOGIN_FAILS: Dict[str, Any] = {}   # ip -> {"n": fail_count, "until": lock_until_ts}
_MAX_FAILS = 5
_LOCK_SECONDS = 60

LOGO_JPG = _b64.b64decode("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b7RWapuDP9Tnnp5I7fThp25ydsjYYGFwkwO2yFte48OacyGZ11tNI39wTk/8SsNV6Ts8H29Q0QPlHFI/8l6Chd0FJyhlt47G+Sx3HxzVejuqzpU6FwoRjT4setCOXOXE3hyW/JbJbJLBr0xkKUs8wuXVFosVPkm8yzY8IqIj/ecFjasWRjf1Mlwkd/jZGwfgSupCupck/g/ueCuNInb56ycPdOMv+1swJCgq874i79WxwH+J2fyVEn0W0nk8/KKi8J5IIiKSgREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAN1MH4UqISngqCXfOB9Qqrap7em3yVsgOFVxTMkaso8mXLqlzupJUzapzRscK15k5io4UZOvnnOS8bWPz9o/eszbtaXW2QNhp6+eCFvRkbuUfXHVcbDsJzrHOjCaxJZN221K5tJdZQqOL702vocpl1vdJz8dbO75yk/mrWbUlXI0h0riD5nKwPPhO8ysatqa5RRt1NbvauesqyfvZkX3WY5+JWz6x7ju4/erXmTmKzKnFdhy53dWfOTKzpnO6nKpl+eqkRZMJGs5uXMdURFJjCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiA//2Q==")

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#000000">
<title>ARAFAT FLEX — Access</title>
<link rel="icon" href="/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@500;600;700&family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>
@property --a{syntax:'<angle>';initial-value:0deg;inherits:false}
:root{--red:#ff1a1a;--rg:rgba(255,26,26,.4);--mut:#8a8a8a;--ok:#2bff88;--fd:'Orbitron',sans-serif;--fr:'Rajdhani','Segoe UI',sans-serif;--fb:'Space Grotesk',system-ui,sans-serif}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;max-width:100%}
body{font-family:var(--fb);background:#000;color:#fff;-webkit-font-smoothing:antialiased;overflow:hidden}
#fx{position:fixed;inset:0;width:100%;height:100%;display:block}
.bgcss{display:none;position:fixed;inset:0;overflow:hidden;background:radial-gradient(circle at 25% 35%,rgba(255,26,26,.28),transparent 45%),radial-gradient(circle at 78% 72%,rgba(255,26,26,.2),transparent 42%);animation:drift 12s ease-in-out infinite alternate}
.bgcss::before,.bgcss::after{content:'';position:absolute;left:50%;top:50%;border-radius:50%;border:1px solid rgba(255,26,26,.35);translate:-50% -50%}
.bgcss::before{width:min(90vw,620px);aspect-ratio:1;animation:spin 40s linear infinite;border-style:dashed}
.bgcss::after{width:min(60vw,400px);aspect-ratio:1;animation:spin 26s linear infinite reverse}
.nogl #fx{display:none}.nogl .bgcss{display:block}
@keyframes drift{to{transform:scale(1.12) translate(2%,-2%)}}
@keyframes spin{to{transform:rotate(360deg)}}
.vig{position:fixed;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 35%,rgba(0,0,0,.75))}
.wrap{position:relative;z-index:2;min-height:100%;min-height:100dvh;display:flex;align-items:center;justify-content:center;padding:24px 18px;overflow-y:auto}
.card{--a:0deg;position:relative;width:min(420px,100%);padding:84px 26px 26px;margin-top:70px;border-radius:28px;text-align:center;background:linear-gradient(180deg,rgba(20,20,20,.62),rgba(4,4,4,.78));backdrop-filter:blur(20px) saturate(140%);-webkit-backdrop-filter:blur(20px) saturate(140%);box-shadow:0 0 70px rgba(255,26,26,.22),0 30px 90px rgba(0,0,0,.8),inset 0 0 0 1px rgba(255,26,26,.28);animation:rise .9s cubic-bezier(.22,1,.36,1) both}
@keyframes rise{from{opacity:0;translate:0 28px;scale:.96}to{opacity:1;translate:0 0;scale:1}}
.card::before{content:'';position:absolute;inset:0;border-radius:inherit;padding:2px;background:conic-gradient(from var(--a),transparent 0 62%,var(--red) 82%,#fff 90%,transparent 100%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box exclude,linear-gradient(#000 0 0);mask-composite:exclude;animation:ang 5s linear infinite;pointer-events:none}
@keyframes ang{to{--a:360deg}}
.logo{position:absolute;left:50%;top:0;width:144px;height:144px;translate:-50% -50%;border-radius:50%;padding:5px}
.logo::before{content:'';position:absolute;inset:0;border-radius:50%;background:conic-gradient(var(--red),transparent 35%,#fff 52%,transparent 68%,var(--red));animation:spin 3.5s linear infinite}
.logo::after{content:'';position:absolute;inset:-16px;border-radius:50%;background:radial-gradient(circle,var(--rg),transparent 68%);filter:blur(10px);z-index:-1;animation:breathe 3.2s ease-in-out infinite}
.logo img{position:relative;z-index:1;width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;background:#000;border:4px solid #000}
@keyframes breathe{0%,100%{opacity:.6;transform:scale(.95)}50%{opacity:1;transform:scale(1.08)}}
h1{font-family:var(--fd);font-weight:900;font-style:italic;font-size:clamp(26px,8vw,34px);letter-spacing:.05em;line-height:1;display:inline-block;transform:skewX(-8deg);text-shadow:0 0 30px var(--rg),0 0 4px rgba(255,255,255,.4)}
.sub{margin-top:10px;font-family:var(--fr);font-size:17px;font-weight:600;color:var(--mut);letter-spacing:.04em}
.lock-line{margin:20px 0 16px;font-size:13.5px;color:var(--mut)}
form{text-align:left}
label{display:block;font-family:var(--fr);font-size:15px;font-weight:700;color:#cfcfcf;margin-bottom:8px}
.field{position:relative;display:flex;align-items:center;height:56px;background:rgba(0,0,0,.65);border:1px solid rgba(255,255,255,.12);border-radius:16px;transition:border-color .2s,box-shadow .2s}
.field:focus-within{border-color:var(--red);box-shadow:0 0 0 4px rgba(255,26,26,.14),0 0 30px rgba(255,26,26,.25)}
.field .ico{width:20px;height:20px;margin-left:16px;color:var(--mut);flex:0 0 auto;transition:color .2s}
.field:focus-within .ico{color:var(--red)}
.field input{flex:1;min-width:0;height:100%;padding:0 10px 0 12px;background:transparent;border:0;outline:0;color:#fff;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:16px;letter-spacing:.2em;text-transform:uppercase}
.field input::placeholder{letter-spacing:.02em;text-transform:none;color:#555;font-family:var(--fb);font-size:16px}
.eye{width:48px;height:100%;background:none;border:0;color:var(--mut);display:grid;place-items:center;cursor:pointer;transition:color .2s}
.eye:hover{color:#fff}.eye svg{width:20px;height:20px}
.err{min-height:22px;margin:10px 2px 0;font-size:13.5px;color:#ff5a5a;font-weight:500}
.btn{position:relative;width:100%;height:56px;margin-top:6px;border:0;border-radius:16px;cursor:pointer;overflow:hidden;color:#fff;font-family:var(--fr);font-size:19px;font-weight:700;letter-spacing:.1em;display:flex;align-items:center;justify-content:center;gap:10px;background:linear-gradient(100deg,#c40000,var(--red));box-shadow:0 10px 34px rgba(255,26,26,.4);transition:transform .15s,box-shadow .25s,filter .2s}
.btn::after{content:'';position:absolute;top:0;bottom:0;width:70px;left:-90px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.4),transparent);transform:skewX(-20deg);transition:left .6s}
.btn:hover{transform:translateY(-2px);box-shadow:0 14px 46px rgba(255,26,26,.65)}.btn:hover::after{left:120%}
.btn:active{transform:scale(.98)}.btn:disabled{cursor:wait;filter:saturate(.6) brightness(.85)}
.btn svg{width:20px;height:20px;transition:transform .2s}.btn:hover svg{transform:translateX(3px)}
.spin{width:20px;height:20px;border:3px solid rgba(255,255,255,.35);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite}
.tag{margin-top:22px;font-family:var(--fr);font-size:15px;font-weight:600;color:var(--mut);letter-spacing:.06em}
.shake{animation:shake .5s cubic-bezier(.36,.07,.19,.97)}
@keyframes shake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-8px)}40%,60%{transform:translateX(8px)}}
.card.bad{box-shadow:0 0 90px rgba(255,26,26,.55),0 30px 90px #000,inset 0 0 0 1px var(--red)}
.card.ok{animation:ok .95s cubic-bezier(.22,1,.36,1) forwards}
.card.ok .logo::before{animation-duration:.6s}
@keyframes ok{40%{box-shadow:0 0 120px rgba(43,255,136,.5),0 30px 90px #000,inset 0 0 0 1px var(--ok)}to{opacity:0;scale:1.1;translate:0 -14px;filter:blur(6px)}}
.flash{position:fixed;inset:0;z-index:5;pointer-events:none;background:radial-gradient(circle at 50% 42%,rgba(255,255,255,.35),rgba(255,26,26,.35) 30%,transparent 65%);opacity:0;transition:opacity .5s}
.flash.on{opacity:1}
@media(max-width:380px){.card{padding-left:18px;padding-right:18px}}
@media(max-height:640px){.card{margin-top:84px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}

/* ================= 2026 THEME LAYER (red + cyan) ================= */
:root{--cy:#00d9ff;--cyg:rgba(0,217,255,.35);--fm:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace}
.bgcss{background:radial-gradient(circle at 25% 35%,rgba(255,26,26,.26),transparent 45%),radial-gradient(circle at 78% 72%,rgba(0,217,255,.16),transparent 42%)}
.card{background:linear-gradient(180deg,rgba(22,22,26,.62),rgba(4,4,6,.80));box-shadow:0 0 70px rgba(255,26,26,.18),0 0 110px rgba(0,217,255,.07),0 30px 90px rgba(0,0,0,.8),inset 0 0 0 1px rgba(255,255,255,.08)}
.card::before{background:conic-gradient(from var(--a),transparent 0 55%,var(--red) 74%,var(--cy) 90%,transparent 100%)}
.logo::before{background:conic-gradient(var(--red),transparent 35%,var(--cy) 52%,transparent 68%,var(--red))}
.logo::after{background:radial-gradient(circle,rgba(255,26,26,.35),rgba(0,217,255,.18) 45%,transparent 70%)}
h1{background:linear-gradient(100deg,#fff 40%,#9ff1ff);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:none;filter:drop-shadow(0 0 18px rgba(255,26,26,.55))}
.sub{color:var(--cy);opacity:.85;letter-spacing:.2em;text-transform:uppercase;font-size:14px}
label{letter-spacing:.14em;text-transform:uppercase;font-size:13px;color:var(--mut)}
.field{background:rgba(0,0,0,.55);border-color:rgba(255,255,255,.1)}
.field:focus-within{border-color:var(--cy);box-shadow:0 0 0 4px rgba(0,217,255,.12),0 0 30px rgba(0,217,255,.22)}
.field:focus-within .ico{color:var(--cy)}
.field input{font-family:var(--fm);letter-spacing:.18em}
.btn{background:linear-gradient(100deg,#c40000,var(--red) 55%,#ff5a3c)}
.trust{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-top:18px}
.trust span{display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border-radius:99px;font-family:var(--fm);font-size:11px;letter-spacing:.04em;color:var(--cy);border:1px solid rgba(0,217,255,.28);background:rgba(0,217,255,.06)}
.trust svg{width:13px;height:13px}
.tag{margin-top:14px;font-size:14px;opacity:.7}
</style>
</head>
<body>
<canvas id="fx" aria-hidden="true"></canvas>
<div class="bgcss" aria-hidden="true"></div>
<div class="vig"></div>
<div class="flash" id="flash"></div>

<div class="wrap">
  <main class="card" id="card">
    <div class="logo"><img src="/logo.jpg" alt="ARAFAT FLEX" width="134" height="134"></div>

    <h1>ARAFAT FLEX</h1>
    <div class="sub">Level Up · Secure access</div>
    <div class="lock-line">Enter your access key to unlock the dashboard.</div>

    <form id="form" autocomplete="off">
      <label for="key">ACCESS KEY</label>
      <div class="field" id="field">
        <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M10.8 12.2 20 3"/><path d="m16 7 3 3"/><path d="m14 9 2 2"/></svg>
        <input id="key" name="key" type="password" placeholder="Type your key" autocomplete="off" autocapitalize="characters" autocorrect="off" spellcheck="false" maxlength="64" required>
        <button class="eye" id="eye" type="button" aria-label="Show key">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>
        </button>
      </div>
      <div class="err" id="err" role="alert" aria-live="polite"></div>
      <button class="btn" id="btn" type="submit"><span id="btnTxt">UNLOCK DASHBOARD</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>
      </button>
    </form>

    <div class="trust">
      <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>Secure session</span>
      <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>30-day sign-in</span>
    </div>
    <div class="tag">Built to flex.</div>
  </main>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>

const $=id=>document.getElementById(id);
const card=$('card'),key=$('key'),err=$('err'),btn=$('btn'),btnTxt=$('btnTxt');
let busy=false,lockTimer=null;

$('eye').addEventListener('click',()=>{const show=key.type==='password';key.type=show?'text':'password';$('eye').setAttribute('aria-label',show?'Hide key':'Show key');key.focus()});
key.addEventListener('input',()=>{err.textContent=''});

function fail(msg){
  err.textContent=msg;window.__fxFail&&window.__fxFail();card.classList.add('bad');setTimeout(()=>card.classList.remove('bad'),700);
  card.classList.remove('shake');void card.offsetWidth;card.classList.add('shake');
  key.select();
}
function startLock(sec){
  clearInterval(lockTimer);
  btn.disabled=true;
  const tick=()=>{if(sec<=0){clearInterval(lockTimer);btn.disabled=false;err.textContent='';btnTxt.textContent='UNLOCK DASHBOARD';return}
    btnTxt.textContent='LOCKED · '+sec+'s';err.textContent='Too many wrong attempts. Please wait.';sec--};
  tick();lockTimer=setInterval(tick,1000);
}

$('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const v=key.value.trim();
  if(busy||btn.disabled)return;
  if(!v){fail('Please enter your access key.');return}
  busy=true;btn.disabled=true;err.textContent='';
  const old=btn.innerHTML;btn.innerHTML='<span class="spin"></span><span>VERIFYING…</span>';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({key:v}),credentials:'same-origin'});
    const d=await r.json().catch(()=>({}));
    if(r.ok&&d.status==='ok'){
      $('flash').classList.add('on');card.classList.add('ok');window.__fxSuccess&&window.__fxSuccess();
      setTimeout(()=>{location.replace('/')},950);
      return;
    }
    btn.innerHTML=old;busy=false;
    if(r.status===429){startLock(Math.max(1,Math.ceil(d.retry_after||60)));return}
    btn.disabled=false;fail(d.error||'Wrong access key. Try again.');
  }catch(ex){
    btn.innerHTML=old;busy=false;btn.disabled=false;fail('Cannot reach the server. Check your connection.');
  }
});
key.focus();


/* 3D background: wireframe core + particle field, reacts to mouse/touch. Falls back to CSS if WebGL/Three.js is unavailable. */
(function(){
  const rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const css=()=>document.body.classList.add('nogl');
  let ok=false;
  try{const t=document.createElement('canvas');ok=!!(window.WebGLRenderingContext&&(t.getContext('webgl')||t.getContext('experimental-webgl')))}catch(e){}
  if(!ok||typeof THREE==='undefined'){css();return}
  let R;
  try{R=new THREE.WebGLRenderer({canvas:$('fx'),antialias:true,alpha:true,powerPreference:'high-performance'})}catch(e){css();return}
  R.setPixelRatio(Math.min(devicePixelRatio||1,2));
  const S=new THREE.Scene(),C=new THREE.PerspectiveCamera(60,1,.1,100);C.position.z=8;
  const core=new THREE.Group();S.add(core);
  const m1=new THREE.MeshBasicMaterial({color:0xff1a1a,wireframe:true,transparent:true,opacity:.4});
  const m2=new THREE.MeshBasicMaterial({color:0x00d9ff,wireframe:true,transparent:true,opacity:.28});
  core.add(new THREE.Mesh(new THREE.IcosahedronGeometry(2.7,1),m1),new THREE.Mesh(new THREE.OctahedronGeometry(1.5,0),m2));
  const n=innerWidth<700?520:1200,pos=new Float32Array(n*3);
  for(let i=0;i<n;i++){const r=4+Math.random()*10,a=Math.random()*6.283,b=Math.acos(2*Math.random()-1);
    pos[i*3]=r*Math.sin(b)*Math.cos(a);pos[i*3+1]=r*Math.sin(b)*Math.sin(a);pos[i*3+2]=r*Math.cos(b)}
  const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pos,3));
  const pm=new THREE.PointsMaterial({color:0xff1a1a,size:.055,transparent:true,opacity:.9,depthWrite:false,blending:THREE.AdditiveBlending});
  const pts=new THREE.Points(pg,pm);S.add(pts);
  const pos2=new Float32Array(Math.floor(n/3)*3);for(let i=0;i<pos2.length;i++)pos2[i]=pos[i];
  const pg2=new THREE.BufferGeometry();pg2.setAttribute('position',new THREE.BufferAttribute(pos2,3));
  const pm2=new THREE.PointsMaterial({color:0x00d9ff,size:.05,transparent:true,opacity:.8,depthWrite:false,blending:THREE.AdditiveBlending});
  const pts2=new THREE.Points(pg2,pm2);pts2.scale.setScalar(1.04);S.add(pts2);
  let mx=0,my=0,tx=0,ty=0,boost=0,warp=0,bad=0,run=true,raf=0;
  const size=()=>{R.setSize(innerWidth,innerHeight,false);C.aspect=innerWidth/innerHeight;C.updateProjectionMatrix();core.scale.setScalar(innerWidth<700?.7:1)};
  size();addEventListener('resize',size);
  addEventListener('pointermove',e=>{tx=e.clientX/innerWidth*2-1;ty=e.clientY/innerHeight*2-1},{passive:true});
  document.addEventListener('visibilitychange',()=>{run=!document.hidden;if(run&&!rm&&!raf)loop()});
  window.__fxSuccess=()=>{boost=1;warp=1};
  window.__fxFail=()=>{bad=1};
  const clock=new THREE.Clock();
  function frame(){
    const dt=Math.min(clock.getDelta(),.05);
    mx+=(tx-mx)*.05;my+=(ty-my)*.05;
    boost*=.96;bad*=.92;
    core.rotation.y+=dt*(.18+boost*3);core.rotation.x+=dt*(.07+boost*1.5);
    pts.rotation.y+=dt*(.02+boost*.6);pts2.rotation.y=-pts.rotation.y*.7;
    S.rotation.y=mx*.35;S.rotation.x=my*.25;
    const s=1+bad*.06*Math.sin(performance.now()/25);core.scale.setScalar((innerWidth<700?.7:1)*s*(1+boost*.35));
    C.position.z=8-warp*4.5;warp*=.97;
    m1.opacity=.4+boost*.5+bad*.4;pm.size=.055+boost*.05;
    R.render(S,C);
  }
  function loop(){raf=0;if(!run||rm)return;frame();raf=requestAnimationFrame(loop)}
  if(rm)frame();else loop();
})();
</script>
</body>
</html>
"""


def _make_session_token(role: str = "admin") -> str:
    exp = str(int(time.time()) + SESSION_DAYS * 86400)
    sig = _hmac.new(_SESSION_SECRET, f"{role}|{exp}".encode(), _hashlib.sha256).hexdigest()
    return f"{role}.{exp}.{sig}"


def _token_role(token: Optional[str]) -> Optional[str]:
    """সঠিক টোকেন হলে role ('admin' / 'user') ফেরত দেয়, নইলে None"""
    if not token:
        return None
    parts = token.split(".")
    if len(parts) != 3:
        return None
    role, exp, sig = parts
    if role not in ("admin", "user") or not exp.isdigit() or int(exp) < time.time():
        return None
    good = _hmac.new(_SESSION_SECRET, f"{role}|{exp}".encode(), _hashlib.sha256).hexdigest()
    return role if _hmac.compare_digest(sig, good) else None


def _client_ip(request: web.Request) -> str:
    fwd = request.headers.get("X-Forwarded-For", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.remote or "?"


def _is_https(request: web.Request) -> bool:
    return request.secure or request.headers.get("X-Forwarded-Proto", "").lower() == "https"


def _session_role(request: web.Request) -> Optional[str]:
    return _token_role(request.cookies.get(SESSION_COOKIE))


def _is_authed(request: web.Request) -> bool:
    return _session_role(request) is not None


# ✅ OWNER ID: প্রতিটি User ব্রাউজারের আলাদা পরিচয় (লগআউট করলেও থাকে) — নিজের যোগ করা আইডি চিনতে লাগে
import secrets as _secrets
OWNER_COOKIE = "afx_owner"


def _sign_owner(oid: str) -> str:
    return _hmac.new(_SESSION_SECRET, ("owner|" + oid).encode(), _hashlib.sha256).hexdigest()[:24]


def _owner_id(request: web.Request) -> Optional[str]:
    raw = request.cookies.get(OWNER_COOKIE, "")
    oid, _, sig = raw.partition(".")
    if oid and sig and _hmac.compare_digest(sig, _sign_owner(oid)):
        return oid
    return None


def _owner_cookie_value(oid: str) -> str:
    return f"{oid}.{_sign_owner(oid)}"


@web.middleware
async def auth_middleware(request: web.Request, handler):
    path = request.path
    if path in ("/login", "/api/login", "/logo.jpg", "/favicon.ico"):
        return await handler(request)
    role = _session_role(request)
    if role:
        request["role"] = role
        # User শুধু দেখতে ও Add Account করতে পারবে — বাকি সব API সার্ভারেই আটকানো
        if role == "user" and path not in USER_ALLOWED_PATHS:
            if path.startswith("/api/"):
                return web.json_response({"status": "error", "error": "Admin access only"}, status=403)
            raise web.HTTPFound("/")
        return await handler(request)
    if path.startswith("/api/"):
        return web.json_response({"status": "error", "error": "unauthorized"}, status=401)
    raise web.HTTPFound("/login")


async def handle_login_page(request: web.Request) -> web.Response:
    if _is_authed(request):
        raise web.HTTPFound("/")
    return web.Response(text=LOGIN_HTML, content_type="text/html", charset="utf-8",
                        headers={"Cache-Control": "no-store"})


async def handle_logo(request: web.Request) -> web.Response:
    return web.Response(body=LOGO_JPG, content_type="image/jpeg",
                        headers={"Cache-Control": "public, max-age=86400"})


async def handle_login(request: web.Request) -> web.Response:
    ip = _client_ip(request)
    now = time.time()
    rec = _LOGIN_FAILS.get(ip, {"n": 0, "until": 0})
    if rec["until"] > now:
        return web.json_response(
            {"status": "error", "error": "Too many attempts", "retry_after": int(rec["until"] - now) + 1},
            status=429)
    try:
        data = await request.json()
    except Exception:
        data = {}
    supplied = str(data.get("key", "")).strip()
    # case-insensitive, constant-time compare
    sup = supplied.upper().encode("utf-8")
    role = None
    if _hmac.compare_digest(sup, DASHBOARD_KEY.upper().encode("utf-8")):
        role = "admin"
    elif _hmac.compare_digest(sup, USER_KEY.upper().encode("utf-8")):
        role = "user"
    if role is None:
        rec["n"] = rec.get("n", 0) + 1
        if rec["n"] >= _MAX_FAILS:
            rec = {"n": 0, "until": now + _LOCK_SECONDS}
            _LOGIN_FAILS[ip] = rec
            return web.json_response(
                {"status": "error", "error": "Too many attempts", "retry_after": _LOCK_SECONDS}, status=429)
        _LOGIN_FAILS[ip] = rec
        left = _MAX_FAILS - rec["n"]
        return web.json_response(
            {"status": "error", "error": f"Wrong access key. {left} attempt(s) left."}, status=401)
    _LOGIN_FAILS.pop(ip, None)
    resp = web.json_response({"status": "ok", "role": role})
    if role == "user" and not _owner_id(request):
        resp.set_cookie(OWNER_COOKIE, _owner_cookie_value(_secrets.token_hex(6)), max_age=365 * 86400,
                        httponly=True, samesite="Lax", secure=_is_https(request), path="/")
    resp.set_cookie(SESSION_COOKIE, _make_session_token(role), max_age=SESSION_DAYS * 86400,
                    httponly=True, samesite="Lax", secure=_is_https(request), path="/")
    return resp


async def handle_logout(request: web.Request) -> web.Response:
    resp = web.json_response({"status": "ok"})
    resp.del_cookie(SESSION_COOKIE, path="/")
    return resp


# Global bot state shared between app.py and Web Dashboard
class BotState:
    def __init__(self):
        self.accounts: Dict[str, Dict[str, Any]] = {}
        self.logs: List[Dict[str, Any]] = []
        self.max_logs = 200
        self.total_matches = 0
        self.total_gained_exp = 0
        self.start_time = time.time()
        self.account_workers: Dict[str, asyncio.Task] = {}
        self.refresh_callbacks: Dict[str, Any] = {}
        self.account_credentials: Dict[str, Dict[str, Any]] = {}
        # ✅ DELETE করা UID গুলো ব্ল্যাকলিস্টে রাখা হয়
        # যাতে চলমান worker পুনরায় register করতে না পারে
        # ✅ FIX: এখন ডিস্কে সেভ হয় — redeploy-এর পরেও টিকে থাকে
        self.deleted_uids_file = os.path.join(BASE_DIR, "deleted_uids.json")
        self.deleted_uids: set = set()
        self._load_deleted_uids()
        # ✅ প্রতিটি UID-এর জন্য আলাদা match type — "BR" বা "LONE_WOLF"
        self.match_types: Dict[str, str] = {}
        # ✅ Global ON/OFF — False হলে কোনো আইডি match search করবে না
        self.global_running: bool = True
        # ✅ AUTO-DELETE: gained_exp এই লিমিট পার হলে আইডি অটো ডিলিট হবে
        self.exp_limit: int = 45000
        # ✅ AUTO-DELETE queue: async cleanup-এর জন্য
        self.auto_delete_queue: set = set()
        # ✅ LEVEL LIMIT: আইডির level এই সংখ্যায় পৌঁছালে dashboard থেকে সরে যাবে (0 = বন্ধ)
        # EXP লিমিটের মতোই accounts.json থেকেও স্থায়ীভাবে মুছে যাবে
        self.level_limit: int = 0
        self.level_remove_queue: set = set()
        # ✅ config-এর guest UID → login-এর পর real account id (app.py সেট করে)
        self.guest_alias: Dict[str, str] = {}
        # ✅ OWNERS: config key (guest UID বা tok_xxxx) → যে User যোগ করেছে তার owner id
        self.owners_file = os.path.join(BASE_DIR, "account_owners.json")
        self.account_owner: Dict[str, str] = {}
        self._load_owners()
        # ✅ USER ADD LIMIT: Admin ঠিক করে প্রতিটি User সর্বোচ্চ কয়টি আইডি রাখতে পারবে (0 = সীমাহীন)
        self.settings_file = os.path.join(BASE_DIR, "dashboard_settings.json")
        self.user_add_limit: int = 0
        self._load_settings()

    def set_match_type(self, uid: str, match_type: str):
        """Dashboard থেকে UID-এর match type সেট করা: 'BR' অথবা 'LONE_WOLF'"""
        uid_str = str(uid)
        allowed = {"BR", "LONE_WOLF"}
        if match_type not in allowed:
            match_type = "LONE_WOLF"
        self.match_types[uid_str] = match_type
        if uid_str in self.accounts:
            self.accounts[uid_str]["match_type"] = match_type
            self.accounts[uid_str]["last_updated"] = time.strftime("%H:%M:%S")

    def get_match_type(self, uid: str) -> str:
        """UID-এর বর্তমান match type পড়া — default LONE_WOLF.
        Level == 2 → auto BR. AUTO_LW_LEVEL (default 3) বা বেশি → auto LONE_WOLF."""
        uid_str = str(uid)
        lvl = self.get_account_level(uid_str)

        # ✅ Level 2 → Auto Battle Royale
        if lvl == 2:
            if self.match_types.get(uid_str) != "BR":
                self.match_types[uid_str] = "BR"
                if uid_str in self.accounts:
                    self.accounts[uid_str]["match_type"] = "BR"
                try:
                    self.log(f"[AUTO] UID {uid_str} Level {lvl} → Battle Royale (BR)", "success", uid_str)
                except Exception:
                    pass
            return "BR"

        # ✅ Level >= AUTO_LW_LEVEL (3) → Auto Lone Wolf
        mt = self.match_types.get(uid_str, "LONE_WOLF")
        if mt == "BR" and AUTO_LW_LEVEL > 0 and lvl >= AUTO_LW_LEVEL:
            self.set_match_type(uid_str, "LONE_WOLF")
            try:
                self.log(f"[AUTO] UID {uid_str} Level {lvl} >= {AUTO_LW_LEVEL} → Lone Wolf (LW)", "success", uid_str)
            except Exception:
                pass
            return "LONE_WOLF"
        return mt

    async def _async_auto_delete(self, uid_str: str):
        """45000 EXP পূর্ণ হওয়া আইডির async cleanup: worker cancel + JSON ফাইল থেকে মুছে ফেলা"""
        try:
            short_key = uid_str.replace("tok_", "")[:10]

            # ✅ STEP 1: bot_state থেকে সরাও
            self.accounts.pop(uid_str, None)
            self.recalc_totals()

            # ✅ STEP 2: accounts*.json ফাইল থেকে atomic delete
            for accounts_file in get_all_account_files_dashboard():
                if not os.path.exists(accounts_file):
                    continue
                try:
                    with open(accounts_file, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                    if not isinstance(existing, list):
                        continue
                    new_list = [
                        acc for acc in existing
                        if str(acc.get("uid", "")).strip() not in self._json_ids(uid_str)
                        and str(acc.get("token", ""))[:10] != short_key
                    ]
                    if len(new_list) < len(existing):
                        tmp_file = accounts_file + ".tmp"
                        with open(tmp_file, "w", encoding="utf-8") as f:
                            json.dump(new_list, f, indent=2, ensure_ascii=False)
                        os.replace(tmp_file, accounts_file)
                except Exception:
                    pass

            # ✅ STEP 3: Worker task বাতিল করো
            for worker_key in [uid_str, short_key]:
                if worker_key in self.account_workers:
                    task = self.account_workers.pop(worker_key)
                    task.cancel()
                    try:
                        await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                        pass

            self.auto_delete_queue.discard(uid_str)
            self.log(f"[AUTO-DELETE] UID {uid_str} → 45000 EXP লিমিট পূর্ণ। আইডি সম্পূর্ণরূপে মুছে ফেলা হয়েছে।", "warning", uid_str)
        except Exception as e:
            self.log(f"[AUTO-DELETE ERROR] UID {uid_str}: {e}", "error", uid_str)

    def _load_deleted_uids(self):
        """redeploy-এর পরেও deleted/level-limit আইডি blacklist-এ থাকবে"""
        try:
            if os.path.exists(self.deleted_uids_file):
                with open(self.deleted_uids_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.deleted_uids = set(str(u) for u in data)
        except Exception:
            self.deleted_uids = set()

    def _save_deleted_uids(self):
        """deleted_uids ডিস্কে সেভ — atomic write"""
        try:
            tmp = self.deleted_uids_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(list(self.deleted_uids), f, ensure_ascii=False)
            os.replace(tmp, self.deleted_uids_file)
        except Exception:
            pass

    def _load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if isinstance(d, dict):
                    self.user_add_limit = max(0, int(d.get("user_add_limit", 0) or 0))
                    # ✅ FIX: রিডিপ্লয়ের পরেও exp_limit ও level_limit টিকে থাকবে
                    saved_exp = d.get("exp_limit", None)
                    if saved_exp is not None:
                        self.exp_limit = max(0, int(saved_exp or 0))
                    saved_lv = d.get("level_limit", None)
                    if saved_lv is not None:
                        self.level_limit = max(0, int(saved_lv or 0))
        except Exception:
            self.user_add_limit = 0

    def _save_settings(self):
        try:
            tmp = self.settings_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump({
                    "user_add_limit": self.user_add_limit,
                    "exp_limit": self.exp_limit,       # ✅ FIX: persist
                    "level_limit": self.level_limit,   # ✅ FIX: persist
                }, f, indent=2)
            os.replace(tmp, self.settings_file)
        except Exception:
            pass

    def count_user_ids(self, owner: str, existing: list) -> int:
        """এই User-এর যোগ করা আইডি, যেগুলো এখনো accounts.json-এ আছে (অটো-ডিলিট/ডিলিট হলে সংখ্যা কমে)"""
        present = set()
        for acc in existing:
            if not isinstance(acc, dict):
                continue
            if acc.get("uid") is not None:
                present.add(str(acc.get("uid")))
            if acc.get("token"):
                present.add("tok_" + str(acc["token"])[:10])
        return sum(1 for k, v in self.account_owner.items() if v == owner and k in present)

    def _load_owners(self):
        try:
            if os.path.exists(self.owners_file):
                with open(self.owners_file, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if isinstance(d, dict):
                    self.account_owner = {str(k): str(v) for k, v in d.items()}
        except Exception:
            self.account_owner = {}

    def _save_owners(self):
        try:
            tmp = self.owners_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.account_owner, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self.owners_file)
        except Exception:
            pass

    def owner_of(self, key: str) -> Optional[str]:
        """ড্যাশবোর্ড key (guest হলে login-এর পর real id) থেকে মালিক খোঁজে"""
        key = str(key)
        o = self.account_owner.get(key)
        if o:
            return o
        for guest, real in self.guest_alias.items():
            if real == key and guest in self.account_owner:
                return self.account_owner[guest]
        return None

    def _json_ids(self, uid_str: str) -> set:
        """accounts.json-এ এই আইডি যে নামে আছে (guest UID হলে login-এর আগের UID-ও)"""
        ids = {uid_str}
        for guest, real in self.guest_alias.items():
            if real == uid_str:
                ids.add(guest)
        return ids

    def _remove_from_json(self, uid_str: str):
        """accounts*.json থেকে আইডি স্থায়ীভাবে মুছে ফেলে (atomic write)"""
        short_key = uid_str.replace("tok_", "")[:10]
        ids = self._json_ids(uid_str)
        for accounts_file in get_all_account_files_dashboard():
            if not os.path.exists(accounts_file):
                continue
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                if not isinstance(existing, list):
                    continue
                new_list = [
                    acc for acc in existing
                    if str(acc.get("uid", "")).strip() not in ids
                    and str(acc.get("token", ""))[:10] != short_key
                ]
                if len(new_list) < len(existing):
                    tmp_file = accounts_file + ".tmp"
                    with open(tmp_file, "w", encoding="utf-8") as f:
                        json.dump(new_list, f, indent=2, ensure_ascii=False)
                    os.replace(tmp_file, accounts_file)
            except Exception:
                pass

    async def _async_level_remove(self, uid_str: str):
        """Level লিমিট পূর্ণ হলে: শুধু worker বন্ধ করা।
        accounts ও JSON check_level_limit()-এই synchronously মুছে ফেলা হয়েছে।"""
        try:
            short_key = uid_str.replace("tok_", "")[:10]
            # ✅ accounts & JSON ইতিমধ্যে check_level_limit()-এ মুছে ফেলা হয়েছে
            # শুধু worker task cancel করতে হবে
            for worker_key in [uid_str, short_key]:
                if worker_key in self.account_workers:
                    task = self.account_workers.pop(worker_key)
                    task.cancel()
                    try:
                        await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                    except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                        pass
            self.log(f"[LEVEL-LIMIT] UID {uid_str} → worker বন্ধ করা হয়েছে।", "warning", uid_str)
        except Exception as e:
            self.log(f"[LEVEL-LIMIT ERROR] UID {uid_str}: {e}", "error", uid_str)
        finally:
            self.level_remove_queue.discard(uid_str)

    def check_level_limit(self, uid_str: str):
        """আইডির level লিমিটে পৌঁছালে সাথে সাথে blacklist করে সরিয়ে দেয়"""
        if self.level_limit <= 0 or uid_str in self.level_remove_queue or uid_str in self.deleted_uids:
            return
        acc = self.accounts.get(uid_str)
        if not acc:
            return
        try:
            lv = int(acc.get("level", 1) or 1)
        except (ValueError, TypeError):
            return
        if lv >= self.level_limit:
            self.level_remove_queue.add(uid_str)
            self.deleted_uids.add(uid_str)      # reload না চাপা পর্যন্ত আর register/start হবে না
            self._save_deleted_uids()           # ✅ FIX: redeploy-এর পরেও blacklist টিকে থাকবে
            self.match_types.pop(uid_str, None)

            # ✅ FIX: Dashboard থেকে সাথে সাথে (synchronously) মুছে ফেলো।
            # আগে শুধু async task-এর উপর নির্ভর করত — task fail হলে account
            # "Offline" হয়ে dashboard-এ রয়ে যেত। এখন এখানেই মুছে যাবে।
            self.accounts.pop(uid_str, None)
            self.recalc_totals()
            self._remove_from_json(uid_str)     # accounts.json থেকেও এখনই মুছে ফেলো
            self.log(
                f"[LEVEL-LIMIT] UID {uid_str} → Lv{lv} (লিমিট: Lv{self.level_limit})। "
                f"আইডি dashboard ও accounts.json থেকে মুছে ফেলা হয়েছে।",
                "warning", uid_str
            )
            # Worker cancel async-এ করা হবে
            try:
                asyncio.get_event_loop().create_task(self._async_level_remove(uid_str))
            except RuntimeError:
                # Event loop না থাকলেও কোনো সমস্যা নেই — account ইতিমধ্যে মুছে গেছে
                self.level_remove_queue.discard(uid_str)

    def enforce_level_limit(self):
        """লিমিট সেট/পরিবর্তনের সময় চলমান সব আইডি যাচাই"""
        for uid_str in list(self.accounts.keys()):
            self.check_level_limit(uid_str)

    def get_account_level(self, uid: str) -> int:
        """UID-এর current level পড়া — default 1"""
        uid_str = str(uid)
        if uid_str in self.accounts:
            return int(self.accounts[uid_str].get("level", 1) or 1)
        return 1

    def log(self, message: str, level: str = "info", uid: Optional[str] = None):
        entry = {
            "time": time.strftime("%H:%M:%S"),
            "level": level,
            "message": message,
            "uid": uid
        }
        self.logs.append(entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def register_account(self, uid: str, nickname: str, region: str, level: int, exp: int, likes: int = 0):
        uid_str = str(uid)
        # ✅ ব্ল্যাকলিস্টে থাকলে re-register করবে না — এটাই মূল সমস্যা ছিল
        if uid_str in self.deleted_uids:
            return
        if uid_str not in self.accounts:
            self.accounts[uid_str] = {
                "uid": uid_str,
                "nickname": nickname or f"Player_{uid_str[:6]}",
                "region": region or "BD",
                "level": level or 1,
                "initial_exp": exp,
                "current_exp": exp,
                "gained_exp": 0,
                "likes": likes or 0,
                "status": "ONLINE",
                "matches_played": 0,
                "active_matches": 0,
                "last_match_time": None,
                "last_updated": time.strftime("%H:%M:%S"),
                "match_type": self.match_types.get(uid_str, "LONE_WOLF")
            }
        else:
            acc = self.accounts[uid_str]
            if nickname:
                acc["nickname"] = nickname
            if region:
                acc["region"] = region
            if level:
                acc["level"] = level
                self.get_match_type(uid_str)   # level barhle BR -> LW auto switch
            acc["current_exp"] = exp
            acc["gained_exp"] = max(0, exp - acc["initial_exp"])
            acc["likes"] = likes
            acc["status"] = "ONLINE"
            acc["last_updated"] = time.strftime("%H:%M:%S")
        self.recalc_totals()
        self.check_level_limit(uid_str)

    def update_exp(self, uid: str, current_exp: int, level: Optional[int] = None):
        uid_str = str(uid)
        # ✅ ডিলিট করা আইডি আপডেট হবে না
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            acc = self.accounts[uid_str]
            old_exp = acc["current_exp"]
            acc["current_exp"] = current_exp
            if level is not None and level > 0:
                acc["level"] = level
                self.get_match_type(uid_str)   # level barhle BR -> LW auto switch
            acc["gained_exp"] = max(0, current_exp - acc["initial_exp"])
            acc["last_updated"] = time.strftime("%H:%M:%S")
            diff = current_exp - old_exp
            if diff > 0:
                self.log(f"Account {acc['nickname']} ({uid_str}) gained +{diff} EXP! Total: +{acc['gained_exp']}", "success", uid_str)
            self.recalc_totals()
            self.check_level_limit(uid_str)

            # ✅ AUTO-DELETE: gained_exp ≥ exp_limit হলে আইডি অটোমেটিক মুছে যাবে
            if self.exp_limit > 0 and acc["gained_exp"] >= self.exp_limit and uid_str not in self.auto_delete_queue:
                self.auto_delete_queue.add(uid_str)
                nickname = acc.get("nickname", uid_str)
                # তৎক্ষণাৎ blacklist করো — worker আর কোনো match খেলবে না
                self.deleted_uids.add(uid_str)
                self._save_deleted_uids()       # ✅ FIX: redeploy-এর পরেও blacklist টিকে থাকবে
                self.match_types.pop(uid_str, None)
                # ✅ FIX: Dashboard ও JSON থেকে সাথে সাথে (synchronously) মুছে ফেলো।
                # আগে শুধু async task-এর উপর নির্ভর করত — task fail হলে account
                # "Offline" হয়ে dashboard-এ রয়ে যেত। এখন level_limit-এর মতোই
                # synchronous removal করা হচ্ছে।
                self.accounts.pop(uid_str, None)
                self.recalc_totals()
                self._remove_from_json(uid_str)
                self.log(
                    f"[AUTO-DELETE] {nickname} ({uid_str}) → {acc['gained_exp']} EXP অর্জন করেছে "
                    f"(লিমিট: {self.exp_limit})। আইডি dashboard ও accounts.json থেকে মুছে ফেলা হয়েছে।",
                    "warning", uid_str
                )
                # Async cleanup: এখন শুধু worker task cancel করতে হবে
                try:
                    asyncio.get_event_loop().create_task(
                        self._async_auto_delete(uid_str)
                    )
                except RuntimeError:
                    self.auto_delete_queue.discard(uid_str)

    def update_status(self, uid: str, status: str, active_matches: Optional[int] = None):
        uid_str = str(uid)
        # ✅ ডিলিট করা আইডি status update হবে না
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            self.accounts[uid_str]["status"] = status
            if status in ("ONLINE", "IN_MATCH", "SEARCHING"):
                self.accounts[uid_str].pop("last_error", None)
            if active_matches is not None:
                self.accounts[uid_str]["active_matches"] = active_matches
            self.accounts[uid_str]["last_updated"] = time.strftime("%H:%M:%S")

    def set_error(self, uid: str, message: str):
        uid_str = str(uid)
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            self.accounts[uid_str]["last_error"] = f"{time.strftime('%H:%M:%S')} - {message}"[:300]

    def set_info(self, uid: str, message: str):
        uid_str = str(uid)
        if uid_str in self.deleted_uids:
            return
        if uid_str in self.accounts:
            self.accounts[uid_str]["last_info"] = f"{time.strftime('%H:%M:%S')} - {message}"[:300]

    def increment_match(self, uid: str):
        uid_str = str(uid)
        self.total_matches += 1
        if uid_str in self.accounts:
            self.accounts[uid_str]["matches_played"] += 1
            self.accounts[uid_str]["last_match_time"] = time.strftime("%H:%M:%S")
            self.accounts[uid_str]["last_updated"] = time.strftime("%H:%M:%S")
            self.log(f"Account {self.accounts[uid_str]['nickname']} finished Match #{self.accounts[uid_str]['matches_played']}", "info", uid_str)

    def recalc_totals(self):
        self.total_gained_exp = sum(acc.get("gained_exp", 0) for acc in self.accounts.values())


bot_state = BotState()


# ==================== HTTP HANDLERS ====================

async def handle_index(request: web.Request) -> web.Response:
    # HTML is embedded — always works regardless of file system state
    return web.Response(text=DASHBOARD_HTML, content_type="text/html", charset="utf-8")


async def handle_get_stats(request: web.Request) -> web.Response:
    role = request.get("role", "admin")
    accounts_data = list(bot_state.accounts.values())
    logs = bot_state.logs[-60:]
    total_matches = bot_state.total_matches
    total_exp = bot_state.total_gained_exp
    if role == "user":
        # ✅ User শুধু নিজের যোগ করা আইডি ও সেগুলোর লগ দেখবে
        me = _owner_id(request)
        accounts_data = [a for a in accounts_data if me and bot_state.owner_of(str(a.get("uid"))) == me]
        logs = [l for l in bot_state.logs if l.get("uid") and me and bot_state.owner_of(str(l["uid"])) == me][-60:]
        total_matches = sum(int(a.get("matches_played", 0) or 0) for a in accounts_data)
        total_exp = sum(int(a.get("gained_exp", 0) or 0) for a in accounts_data)
    # ✅ বেশি লেভেল উপরে (descending); একই লেভেল হলে বেশি gained EXP আগে
    accounts_data.sort(key=lambda x: (int(x.get("level", 0) or 0), x.get("gained_exp", 0)), reverse=True)
    return web.json_response({
        "total_accounts": len(accounts_data),
        "total_matches": total_matches,
        "total_gained_exp": total_exp,
        "accounts": accounts_data,
        "logs": logs,
        "uptime": int(time.time() - bot_state.start_time),
        "global_running": bot_state.global_running,
        "exp_limit": bot_state.exp_limit,
        "level_limit": bot_state.level_limit,
        "user_add_limit": bot_state.user_add_limit,
        "role": role
    })


def _check_user_limit(role: str, owner: Optional[str], owner_key: str, existing: list) -> Optional[str]:
    """User-এর আইডি লিমিট পূর্ণ হলে error মেসেজ ফেরত দেয়। Admin-এর কোনো লিমিট নেই।"""
    lim = bot_state.user_add_limit
    if role != "user" or lim <= 0 or not owner:
        return None
    # নিজের আগে যোগ করা আইডি আবার যোগ করলে নতুন স্লট লাগে না
    if bot_state.account_owner.get(owner_key) == owner:
        return None
    if bot_state.count_user_ids(owner, existing) >= lim:
        return f"ID limit reached. You can add up to {lim} ID(s) only."
    return None


async def handle_add_account(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        role = request.get("role", "admin")
        new_owner_cookie = None
        owner = None
        if role == "user":
            owner = _owner_id(request)
            if not owner:
                owner = _secrets.token_hex(6)
                new_owner_cookie = _owner_cookie_value(owner)
        accounts_file = ACCOUNTS_FILE_PATH
        existing = []
        if os.path.exists(accounts_file):
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        if "uid" in data and "password" in data:
            uid = str(data["uid"]).strip()
            pwd = str(data["password"]).strip()
            if not uid or not pwd:
                return web.json_response({"status": "error", "error": "UID and Password are required"})
            owner_key = uid
            if role == "user" and (any(str(acc.get("uid")) == uid for acc in existing) or uid in bot_state.accounts) \
                    and bot_state.account_owner.get(uid) != owner:
                return web.json_response({"status": "error", "error": "This account already exists"})
            lim_err = _check_user_limit(role, owner, owner_key, existing)
            if lim_err:
                return web.json_response({"status": "error", "error": lim_err})
            existing = [acc for acc in existing if str(acc.get("uid")) != uid]
            existing.append({"uid": uid, "password": pwd})
            # ✅ Re-add করলে blacklist থেকে সরাও — না হলে আর চালু হবে না
            bot_state.deleted_uids.discard(uid)
            bot_state._save_deleted_uids()  # ✅ FIX: ফাইল থেকেও সরাও
        elif "token" in data:
            token = str(data["token"]).strip()
            if not token:
                return web.json_response({"status": "error", "error": "Token is required"})
            owner_key = f"tok_{token[:10]}"
            if role == "user" and (any(acc.get("token") == token for acc in existing) or owner_key in bot_state.accounts) \
                    and bot_state.account_owner.get(owner_key) != owner:
                return web.json_response({"status": "error", "error": "This account already exists"})
            lim_err = _check_user_limit(role, owner, owner_key, existing)
            if lim_err:
                return web.json_response({"status": "error", "error": lim_err})
            existing = [acc for acc in existing if acc.get("token") != token]
            existing.append({"token": token})
            # ✅ Token re-add করলে blacklist থেকে সরাও
            bot_state.deleted_uids.discard(token[:10])
            bot_state.deleted_uids.discard(f"tok_{token[:10]}")
            bot_state._save_deleted_uids()  # ✅ FIX: ফাইল থেকেও সরাও
        else:
            return web.json_response({"status": "error", "error": "Invalid payload"})

        with open(accounts_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        # মালিক নথিভুক্ত করো (User হলে) — Admin যোগ করলে মালিক থাকে না, শুধু Admin দেখবে
        if role == "user" and owner:
            bot_state.account_owner[owner_key] = owner
            bot_state._save_owners()
        elif role == "admin":
            if bot_state.account_owner.pop(owner_key, None) is not None:
                bot_state._save_owners()

        bot_state.log(f"New account added: {data.get('uid') or 'Token'}", "success", owner_key)

        # Trigger dynamic worker launch
        if "on_account_added" in bot_state.refresh_callbacks:
            asyncio.create_task(bot_state.refresh_callbacks["on_account_added"](data))

        resp = web.json_response({"status": "ok"})
        if new_owner_cookie:
            resp.set_cookie(OWNER_COOKIE, new_owner_cookie, max_age=365 * 86400,
                            httponly=True, samesite="Lax", secure=_is_https(request), path="/")
        return resp
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_delete_account(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        uid = str(data.get("uid", "")).strip()
        if not uid:
            return web.json_response({"status": "error", "error": "uid missing"})

        # token-based worker key: "tok_abcdefghij" → "abcdefghij"
        short_key = uid.replace("tok_", "")[:10]

        # ✅ সব accounts*.json ফাইলে খুঁজে atomic write দিয়ে delete করে
        for accounts_file in get_all_account_files_dashboard():
            if not os.path.exists(accounts_file):
                continue
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                if not isinstance(existing, list):
                    continue

                new_list = [
                    acc for acc in existing
                    if str(acc.get("uid", "")).strip() != uid
                    and str(acc.get("token", ""))[:10] != short_key
                ]

                if len(new_list) < len(existing):
                    # ✅ Atomic write — crash হলে ফাইল নষ্ট হবে না
                    tmp_file = accounts_file + ".tmp"
                    with open(tmp_file, "w", encoding="utf-8") as f:
                        json.dump(new_list, f, indent=2, ensure_ascii=False)
                    os.replace(tmp_file, accounts_file)
            except Exception:
                pass

        # ✅ STEP 1: আগেই ব্ল্যাকলিস্টে যোগ করো
        # এর ফলে চলমান worker আর re-register করতে পারবে না
        bot_state.deleted_uids.add(uid)
        bot_state.deleted_uids.add(short_key)
        bot_state._save_deleted_uids()  # ✅ FIX: redeploy-এর পরেও blacklist টিকে থাকবে

        # ✅ STEP 2: bot_state থেকে সরাও এবং totals আপডেট করো
        if uid in bot_state.accounts:
            del bot_state.accounts[uid]
            bot_state.recalc_totals()

        # ✅ STEP 3: Worker বাতিল করো এবং সম্পূর্ণভাবে await করো
        # break ছিল আগে — এর ফলে দুটো key-এর একটাই cancel হতো
        # এখন দুটোই cancel করা হবে এবং properly await করা হবে
        for worker_key in [uid, short_key]:
            if worker_key in bot_state.account_workers:
                task = bot_state.account_workers.pop(worker_key)
                task.cancel()
                try:
                    await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                    pass  # cancel হয়েছে — এটাই স্বাভাবিক

        bot_state.log(f"Account {uid} deleted from dashboard and accounts.json.", "warning", uid)
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_refresh_account(request: web.Request) -> web.Response:
    try:
        data = await request.json()
        uid = str(data.get("uid")).strip()
        if "on_refresh_account" in bot_state.refresh_callbacks:
            asyncio.create_task(bot_state.refresh_callbacks["on_refresh_account"](uid))
        return web.json_response({"status": "ok"})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_reload_accounts(request: web.Request) -> web.Response:
    """
    accounts*.json ফাইল থেকে নতুন করে সব account load করে।
    - deleted_uids blacklist পুরোপুরি clear হয়
    - যে accounts এখন চলছে না কিন্তু JSON এ আছে সেগুলো স্বয়ংক্রিয়ভাবে চালু হয়
    - ইতিমধ্যে চলমান accounts অপরিবর্তিত থাকে
    """
    try:
        # ✅ STEP 1: পুরো blacklist clear করো
        cleared = len(bot_state.deleted_uids)
        bot_state.deleted_uids.clear()
        bot_state.level_remove_queue.clear()
        bot_state._save_deleted_uids()  # ✅ FIX: ফাইলও clear করো

        # ✅ STEP 2: app.py-এর reload callback ডাকো
        added = 0
        if "on_reload_accounts" in bot_state.refresh_callbacks:
            added = await bot_state.refresh_callbacks["on_reload_accounts"]()

        msg = f"Reload complete: {cleared} blacklisted UIDs cleared, {added} new account(s) started."
        bot_state.log(msg, "success")
        return web.json_response({"status": "ok", "message": msg, "cleared": cleared, "started": added})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_set_match_type(request: web.Request) -> web.Response:
    """Dashboard থেকে UID-এর match type পরিবর্তন করা: BR অথবা LONE_WOLF"""
    try:
        data = await request.json()
        uid = str(data.get("uid", "")).strip()
        match_type = str(data.get("match_type", "LONE_WOLF")).strip().upper()
        if not uid:
            return web.json_response({"status": "error", "error": "UID required"}, status=400)
        if match_type not in ("BR", "LONE_WOLF"):
            return web.json_response({"status": "error", "error": "Invalid match_type. Use BR or LONE_WOLF"}, status=400)
        bot_state.set_match_type(uid, match_type)
        label = "⚔ Battle Royale" if match_type == "BR" else "🐺 Lone Wolf"
        bot_state.log(f"[MATCH TYPE] UID {uid} → {label}", "info", uid)
        return web.json_response({"status": "ok", "uid": uid, "match_type": match_type})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_toggle_global(request: web.Request) -> web.Response:
    """সব আইডি ON/OFF করা — running=true হলে ম্যাচ শুরু, false হলে বন্ধ"""
    try:
        data = await request.json()
        running = bool(data.get("running", True))
        bot_state.global_running = running
        state_str = "চালু (ON)" if running else "বন্ধ (OFF)"
        bot_state.log(f"[GLOBAL] সব বট {state_str} করা হয়েছে", "success" if running else "warning")

        # If turning OFF, update all account statuses to PAUSED
        if not running:
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    status = bot_state.accounts[uid_str].get("status", "ONLINE")
                    if status not in ("OFFLINE", "ERROR", "CONNECTING"):
                        bot_state.accounts[uid_str]["status"] = "PAUSED"
        else:
            # Turning ON — reset PAUSED statuses to ONLINE
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    if bot_state.accounts[uid_str].get("status") == "PAUSED":
                        bot_state.accounts[uid_str]["status"] = "ONLINE"

        return web.json_response({"status": "ok", "running": running})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_all_mode(request: web.Request) -> web.Response:
    """ড্যাশবোর্ডের সব আইডির match type একসাথে পরিবর্তন করা"""
    try:
        data = await request.json()
        mode = str(data.get("mode", "LONE_WOLF")).strip().upper()
        if mode not in ("BR", "LONE_WOLF", "AUTO"):
            return web.json_response({"status": "error", "error": "Invalid mode. Use BR, LONE_WOLF or AUTO"}, status=400)

        changed = 0
        if mode == "AUTO":
            # ✅ AUTO: সব আইডির manually-forced match_type সরিয়ে দেওয়া
            # get_match_type() এর Level-based auto-logic আবার কাজ করবে
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    # match_types থেকে সরালে get_match_type() নিজেই level দেখে সিদ্ধান্ত নেবে
                    bot_state.match_types.pop(uid_str, None)
                    if uid_str in bot_state.accounts:
                        lvl = bot_state.get_account_level(uid_str)
                        auto_mt = "BR" if lvl == 2 else "LONE_WOLF"
                        bot_state.accounts[uid_str]["match_type"] = auto_mt
                    changed += 1
            label = "🔄 Auto Level Mode"
        else:
            for uid_str in list(bot_state.accounts.keys()):
                if uid_str not in bot_state.deleted_uids:
                    bot_state.set_match_type(uid_str, mode)
                    changed += 1
            label = "⚔ Battle Royale" if mode == "BR" else "🐺 Lone Wolf"

        bot_state.log(f"[GLOBAL MODE] সব {changed}টি আইডি → {label}", "success")
        return web.json_response({"status": "ok", "mode": mode, "changed": changed})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_exp_limit(request: web.Request) -> web.Response:
    """EXP লিমিট আপডেট করা — এই সীমা পার হলে আইডি অটো ডিলিট হবে"""
    try:
        data = await request.json()
        raw = data.get("exp_limit", None)
        if raw is None:
            return web.json_response({"status": "error", "error": "exp_limit missing"}, status=400)
        try:
            limit = int(str(raw).strip().replace(",", ""))
        except (ValueError, TypeError):
            return web.json_response({"status": "error", "error": "exp_limit must be a number"}, status=400)
        if limit < 0:
            return web.json_response({"status": "error", "error": "exp_limit cannot be negative"}, status=400)
        bot_state.exp_limit = limit
        bot_state._save_settings()  # ✅ FIX: redeploy-এর পরেও টিকে থাকবে
        msg = f"EXP লিমিট সেট: {limit:,}" if limit > 0 else "EXP লিমিট বন্ধ (0 = কোনো লিমিট নেই)"
        bot_state.log(f"[EXP LIMIT] {msg}", "success")
        return web.json_response({"status": "ok", "exp_limit": limit})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_level_limit(request: web.Request) -> web.Response:
    """Level লিমিট সেট — আইডি এই level-এ পৌঁছালে dashboard থেকে সরে যাবে (0 = বন্ধ)"""
    try:
        data = await request.json()
        raw = data.get("level_limit", None)
        if raw is None:
            return web.json_response({"status": "error", "error": "level_limit missing"}, status=400)
        try:
            limit = int(str(raw).strip())
        except (ValueError, TypeError):
            return web.json_response({"status": "error", "error": "level_limit must be a number"}, status=400)
        if limit == 1 or limit < 0 or limit > 200:
            return web.json_response({"status": "error", "error": "Level লিমিট 0 (বন্ধ) অথবা 2 থেকে 200 এর মধ্যে দিন"}, status=400)
        bot_state.level_limit = limit
        bot_state._save_settings()  # ✅ FIX: redeploy-এর পরেও টিকে থাকবে
        msg = f"Level লিমিট সেট: Lv{limit}" if limit > 0 else "Level লিমিট বন্ধ (0 = কোনো লিমিট নেই)"
        bot_state.log(f"[LEVEL LIMIT] {msg}", "success")
        bot_state.enforce_level_limit()
        return web.json_response({"status": "ok", "level_limit": limit})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_set_user_limit(request: web.Request) -> web.Response:
    """প্রতিটি User সর্বোচ্চ কয়টি আইডি যোগ করতে পারবে — শুধু Admin ঠিক করে (0 = সীমাহীন)"""
    try:
        data = await request.json()
        raw = data.get("user_add_limit", None)
        if raw is None:
            return web.json_response({"status": "error", "error": "user_add_limit missing"}, status=400)
        try:
            limit = int(str(raw).strip())
        except (ValueError, TypeError):
            return web.json_response({"status": "error", "error": "user_add_limit must be a number"}, status=400)
        if limit < 0 or limit > 100000:
            return web.json_response({"status": "error", "error": "user_add_limit must be 0 to 100000"}, status=400)
        bot_state.user_add_limit = limit
        bot_state._save_settings()
        msg = f"প্রতি User সর্বোচ্চ {limit}টি আইডি" if limit > 0 else "User ID লিমিট বন্ধ (0 = সীমাহীন)"
        bot_state.log(f"[USER LIMIT] {msg}", "success")
        return web.json_response({"status": "ok", "user_add_limit": limit})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_clear_logs(request: web.Request) -> web.Response:
    """Activity Log পরিষ্কার করা"""
    bot_state.logs.clear()
    return web.json_response({"status": "ok"})


# ==================== JSON DATABASE MANAGEMENT (Admin only) ====================
# Dashboard theke accounts.json upload / delete / download. Auto-backup shoho.
# Admin-only: USER_ALLOWED_PATHS-e nei, tai auth_middleware user-ke 403 dey.
import shutil as _shutil
from datetime import datetime as _dt

JSON_MAX_BYTES = 2 * 1024 * 1024          # 2 MB upload limit
JSON_BACKUP_DIR = os.path.join(BASE_DIR, "data", "backups")
JSON_BACKUP_KEEP = 20                     # purono backup auto-clean


def _json_entry_keys(acc: Any):
    """accounts.json entry theke dashboard key-gulo (uid / tok_xxx / short token)"""
    keys = set()
    if not isinstance(acc, dict):
        return keys
    uid = str(acc.get("uid", "") or "").strip()
    tok = str(acc.get("token", "") or "").strip()
    if uid:
        keys.add(uid)
    if tok:
        keys.update({tok[:10], f"tok_{tok[:10]}"})
    return keys


def _json_validate(data: Any):
    """list / {"accounts": [...]} nei -> (clean_list, error)"""
    if isinstance(data, dict) and isinstance(data.get("accounts"), list):
        data = data["accounts"]
    if not isinstance(data, list):
        return None, "File must contain a JSON list of accounts"
    clean, bad = [], 0
    for acc in data:
        if not isinstance(acc, dict):
            bad += 1
            continue
        uid = str(acc.get("uid", "") or "").strip()
        pwd = str(acc.get("password", "") or "").strip()
        tok = str(acc.get("token", "") or "").strip()
        if uid and pwd:
            clean.append({"uid": uid, "password": pwd})
        elif tok:
            clean.append({"token": tok})
        else:
            bad += 1
    if bad:
        return None, f"{bad} invalid entr{'y' if bad == 1 else 'ies'} (each needs uid+password or token)"
    if not clean:
        return None, "No accounts found in file"
    # duplicate remove (last wins)
    seen, out = set(), []
    for acc in reversed(clean):
        k = acc.get("uid") or acc.get("token")
        if k in seen:
            continue
        seen.add(k)
        out.append(acc)
    out.reverse()
    return out, None


def _json_backup(path: str) -> Optional[str]:
    """path-er copy data/backups/-e rakhe; purono gulo clean kore"""
    if not os.path.exists(path):
        return None
    os.makedirs(JSON_BACKUP_DIR, exist_ok=True)
    stamp = _dt.now().strftime("%Y%m%d_%H%M%S_%f")[:19]   # ms precision: same-second backup overwrite hobe na
    dest = os.path.join(JSON_BACKUP_DIR, f"accounts_backup_{stamp}.json")
    _shutil.copy2(path, dest)
    try:
        olds = sorted(_glob.glob(os.path.join(JSON_BACKUP_DIR, "accounts_backup_*.json")))
        for old in olds[:-JSON_BACKUP_KEEP]:
            os.remove(old)
    except Exception:
        pass
    return os.path.basename(dest)


def _json_atomic_write(path: str, data: Any):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def _json_read_list(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict):
            d = d.get("accounts", [])
        return d if isinstance(d, list) else []
    except Exception:
        return []


async def _json_stop_orphans() -> int:
    """JSON file-e ar nei emon account-er worker bondho + dashboard theke soriye dey"""
    keep = set()
    for fp in get_all_account_files_dashboard():
        for acc in _json_read_list(fp):
            keep |= _json_entry_keys(acc)
    removed = 0
    for key in list(bot_state.accounts.keys()):
        short = key.replace("tok_", "")[:10]
        aliases = {g for g, real in bot_state.guest_alias.items() if real == key}
        if key in keep or short in keep or (aliases & keep):
            continue
        bot_state.deleted_uids.add(key)
        bot_state.deleted_uids.add(short)
        bot_state.accounts.pop(key, None)
        for wk in {key, short, *aliases}:
            task = bot_state.account_workers.pop(wk, None)
            if task:
                task.cancel()
                try:
                    await asyncio.wait_for(asyncio.shield(task), timeout=3.0)
                except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                    pass
        removed += 1
    if removed:
        bot_state._save_deleted_uids()
        bot_state.recalc_totals()
    return removed


async def handle_json_info(request: web.Request) -> web.Response:
    try:
        path = ACCOUNTS_FILE_PATH
        files = get_all_account_files_dashboard()
        info = {"status": "ok", "name": os.path.basename(path), "exists": os.path.exists(path),
                "size": 0, "count": 0, "modified": None,
                "total_files": len(files), "total_count": 0, "backups": 0}
        if info["exists"]:
            st = os.stat(path)
            info["size"] = st.st_size
            info["modified"] = _dt.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
            info["count"] = len(_json_read_list(path))
        info["total_count"] = sum(len(_json_read_list(fp)) for fp in files if os.path.exists(fp))
        info["backups"] = len(_glob.glob(os.path.join(JSON_BACKUP_DIR, "accounts_backup_*.json")))
        return web.json_response(info)
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})


async def handle_json_upload(request: web.Request) -> web.Response:
    """multipart 'file' + ?mode=replace|merge"""
    try:
        mode = request.query.get("mode", "replace")
        if mode not in ("replace", "merge"):
            mode = "replace"
        reader = await request.multipart()
        field = await reader.next()
        if field is None or field.name != "file":
            return web.json_response({"status": "error", "error": "No file provided"}, status=400)
        buf = bytearray()
        while True:
            chunk = await field.read_chunk(64 * 1024)
            if not chunk:
                break
            buf.extend(chunk)
            if len(buf) > JSON_MAX_BYTES:
                return web.json_response({"status": "error", "error": "File too large (max 2 MB)"}, status=413)
        try:
            raw = json.loads(bytes(buf).decode("utf-8-sig"))
        except Exception as e:
            return web.json_response({"status": "error", "error": f"Invalid JSON: {e}"}, status=400)
        new_list, err = _json_validate(raw)
        if err:
            return web.json_response({"status": "error", "error": err}, status=400)

        path = ACCOUNTS_FILE_PATH
        backup = _json_backup(path)
        final = new_list
        if mode == "merge":
            merged = {}
            for acc in _json_read_list(path) + new_list:
                merged[acc.get("uid") or acc.get("token")] = acc
            final = list(merged.values())
        _json_atomic_write(path, final)

        # blacklist theke uploaded id-gulo soraw, tarpor reload callback e notun worker chalu
        for acc in final:
            for k in _json_entry_keys(acc):
                bot_state.deleted_uids.discard(k)
        bot_state._save_deleted_uids()
        removed = await _json_stop_orphans() if mode == "replace" else 0
        started = 0
        if "on_reload_accounts" in bot_state.refresh_callbacks:
            started = await bot_state.refresh_callbacks["on_reload_accounts"]()

        msg = f"accounts.json {mode}d: {len(final)} account(s), {started} started, {removed} removed."
        bot_state.log(msg, "success")
        return web.json_response({"status": "ok", "count": len(final), "started": started,
                                  "removed": removed, "backup": backup, "message": msg})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_json_delete(request: web.Request) -> web.Response:
    """accounts.json khali kore (file-ta thake, content = []) + backup + worker stop"""
    try:
        data = await request.json()
        if data.get("confirm") is not True:
            return web.json_response({"status": "error", "error": "Confirmation required"}, status=400)
        path = ACCOUNTS_FILE_PATH
        count = len(_json_read_list(path))
        backup = _json_backup(path)
        _json_atomic_write(path, [])
        removed = await _json_stop_orphans()
        msg = f"accounts.json cleared ({count} account(s)). {removed} worker(s) stopped."
        bot_state.log(msg, "warning")
        return web.json_response({"status": "ok", "deleted": count, "removed": removed,
                                  "backup": backup, "message": msg})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)


async def handle_json_download(request: web.Request) -> web.Response:
    try:
        if not os.path.exists(ACCOUNTS_FILE_PATH):
            return web.json_response({"status": "error", "error": "accounts.json not found"}, status=404)
        with open(ACCOUNTS_FILE_PATH, "rb") as f:
            body = f.read()
        return web.Response(body=body, content_type="application/json",
                            headers={"Content-Disposition": 'attachment; filename="accounts.json"'})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)



async def start_web_dashboard(host: str = "0.0.0.0", port: int = 6243):
    app = web.Application(middlewares=[auth_middleware])
    app.router.add_get("/login", handle_login_page)
    app.router.add_post("/api/login", handle_login)
    app.router.add_post("/api/logout", handle_logout)
    app.router.add_get("/logo.jpg", handle_logo)
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/stats", handle_get_stats)
    app.router.add_post("/api/account/add", handle_add_account)
    app.router.add_post("/api/account/delete", handle_delete_account)
    app.router.add_post("/api/account/refresh", handle_refresh_account)
    app.router.add_post("/api/accounts/reload", handle_reload_accounts)
    app.router.add_post("/api/account/match-type", handle_set_match_type)
    app.router.add_post("/api/bot/toggle", handle_toggle_global)
    app.router.add_post("/api/accounts/set-all-mode", handle_set_all_mode)
    app.router.add_post("/api/settings/exp-limit", handle_set_exp_limit)
    app.router.add_post("/api/settings/level-limit", handle_set_level_limit)
    app.router.add_post("/api/settings/user-limit", handle_set_user_limit)
    app.router.add_post("/api/logs/clear", handle_clear_logs)
    app.router.add_post("/api/json/info", handle_json_info)
    app.router.add_post("/api/json/upload", handle_json_upload)
    app.router.add_post("/api/json/delete", handle_json_delete)
    app.router.add_get("/api/json/download", handle_json_download)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"\033[92m[+] Web Dashboard running on http://localhost:{port}\033[0m")
