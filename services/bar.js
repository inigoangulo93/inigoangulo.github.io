/* Header states shared by the service and writing pages: full at the top, island when scrolled, mini pill when scrolling down. */
(function(){var bar=document.querySelector('.bar');if(!bar)return;var state='full',lastY=window.scrollY||0,acc=0;
function set(st){if(st===state)return;state=st;bar.classList.toggle('bar--island',st!=='full');bar.classList.toggle('bar--mini',st==='mini')}
function upd(){var y=window.scrollY||document.documentElement.scrollTop;var dy=y-lastY;lastY=y;
  if(y<=40){set('full');acc=0;return}
  if(dy>0){acc=Math.max(0,acc)+dy;if(y>220&&acc>12)set('mini');else if(state==='full')set('island')}
  else if(dy<0){acc=Math.min(0,acc)+dy;if(acc<-10)set('island');else if(state==='full')set('island')}
  else if(state==='full')set('island');}
window.addEventListener('scroll',upd,{passive:true});window.addEventListener('resize',upd,{passive:true});upd();
bar.addEventListener('click',function(e){if(state==='mini'){e.preventDefault();set('island');acc=0}});
if(window.matchMedia&&window.matchMedia('(hover:hover) and (pointer:fine)').matches){bar.addEventListener('mouseenter',function(){if(state==='mini')bar.classList.add('bar--peek')});bar.addEventListener('mouseleave',function(){bar.classList.remove('bar--peek')})}
})();
