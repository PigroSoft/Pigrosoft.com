/* PIGRUN.EXE
   A small endless runner. The pig plays itself when the page loads; a click,
   tap or Space hands control to the visitor. Nothing is stored: the best
   score lives only as long as the page is open. */
(function () {
  "use strict";

  var canvas = document.getElementById("pigrun");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var box = canvas.parentElement;

  var COLORS = {
    K: "#000000", P: "#F7A8C4", L: "#FFD9E6", D: "#D9668F", S: "#EE86AB",
    N: "#7A2848", E: "#000000", W: "#FFFFFF", R: "#D93025", G: "#BDB6A4",
    Y: "#F2C230", M: "#5A1F3A"
  };
  var PAPER = "#FFFDF5", LINE = "#8E8776", CLOUD = "#EDE7D8";

  /* Sprites are drawn as filled shapes; the black outline is added here. */
  function sprite(rows) {
    var h = rows.length + 2, w = rows[0].length + 2, grid = [], x, y;
    for (y = 0; y < h; y++) {
      grid.push([]);
      for (x = 0; x < w; x++) {
        var c = rows[y - 1] && rows[y - 1][x - 1];
        grid[y].push(c && c !== "." ? c : ".");
      }
    }
    var filled = function (x, y) { return grid[y] && grid[y][x] && grid[y][x] !== "." && grid[y][x] !== "o"; };
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      if (grid[y][x] === "." && (filled(x + 1, y) || filled(x - 1, y) || filled(x, y + 1) || filled(x, y - 1))) grid[y][x] = "o";
    }
    var c2 = document.createElement("canvas");
    c2.width = w; c2.height = h;
    var g = c2.getContext("2d");
    for (y = 0; y < h; y++) for (x = 0; x < w; x++) {
      var ch = grid[y][x];
      if (ch === ".") continue;
      g.fillStyle = ch === "o" ? COLORS.K : COLORS[ch];
      g.fillRect(x, y, 1, 1);
    }
    return { img: c2, w: w, h: h };
  }

  var BODY = [
    "...............PP....",
    "..............PPP....",
    "D...PPPPPPPPPPPPP....",
    ".D.PPPPPPPPPPPPPPPP..",
    "..PLLPPPPPPPPPPPPPPSS",
    "..PLPPPPPPPPPPPEPPSNS",
    "..PPPPPPPPPPPPPPPPSSS",
    "..PPPPPPPPPPPPPPPPP..",
    "...DPPPPPPPPPPPPPPD..",
    "...DDDDDDDDDDDDDDDD.."
  ];
  var LEGS = {
    a: ["....DD.........DD....", "....DD.........DD...."],
    b: [".....DD.........DD...", "......D..........D..."],
    up: ["...DD..........DD....", "..DD..........DD....."]
  };
  var PIG = {
    a: sprite(BODY.concat(LEGS.a)),
    b: sprite(BODY.concat(LEGS.b)),
    up: sprite(BODY.concat(LEGS.up))
  };
  var CLOCK = sprite([
    ".R.......R.",
    "RRR.....RRR",
    ".RRRRRRRRR.",
    "RWWWWWWWWWR",
    "RWWWWKWWWWR",
    "RWWWWKWWWWR",
    "RWWWWKKKWWR",
    "RWWWWWWWWWR",
    ".RWWWWWWWR.",
    "..RRRRRRR..",
    ".R.......R."
  ]);
  var PAPERS = sprite([
    "WWWWWWW.",
    "WGGGGGW.",
    "WWWWWWW.",
    "WGGGWWW.",
    ".WWWWWWW",
    ".WGGGGGW",
    ".WWWWWWW",
    ".WGGGGWW",
    "WWWWWWW.",
    "WGGGGGW.",
    "WWWWWWW.",
    "WGGGWWW.",
    "WWWWWWW."
  ]);
  var OBSTACLES = [CLOCK, CLOCK, PAPERS];

  /* World, in logical pixels. One logical pixel is drawn as SCALE screen pixels. */
  var H = 68, GROUND = 60, PIG_X = 14;
  var GRAVITY = 0.5, JUMP = -6.0, START = 2.6, MAX = 5.4, ACCEL = 0.0012;
  var W = 280, SCALE = 3;

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var g = {
    mode: reduced ? "still" : "demo", speed: START, score: 0, hi: 0,
    y: GROUND, vy: 0, run: 0, obs: [], gap: 80, clouds: [], dots: [], overAt: 0
  };
  window.__pigrun = { demoCrashes: 0 };

  function size() {
    var css = box.clientWidth;
    SCALE = css < 480 ? 2 : 3;
    W = Math.max(140, Math.floor(css / SCALE));
    var dpr = window.devicePixelRatio || 1;
    canvas.style.width = W * SCALE + "px";
    canvas.style.height = H * SCALE + "px";
    canvas.width = Math.round(W * SCALE * dpr);
    canvas.height = Math.round(H * SCALE * dpr);
    ctx.setTransform(SCALE * dpr, 0, 0, SCALE * dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
    draw();
  }

  function reset() {
    g.speed = START; g.score = 0; g.y = GROUND; g.vy = 0; g.obs = []; g.gap = 70;
    g.clouds = [{ x: W * 0.3, y: 12 }, { x: W * 0.75, y: 20 }];
    g.dots = [];
    for (var i = 0; i < W; i += 9 + (i * 7) % 13) g.dots.push({ x: i, y: GROUND + 3 + (i % 3) });
  }

  function jump() {
    if (g.y >= GROUND) g.vy = JUMP;
  }

  function nextObstacle() {
    for (var i = 0; i < g.obs.length; i++) {
      var o = g.obs[i];
      if (o.x + o.s.w > PIG_X + 2) return o;
    }
    return null;
  }

  function step(dt) {
    var move = g.speed * dt;
    g.speed = Math.min(MAX, g.speed + ACCEL * dt);
    g.run += move;

    g.obs.forEach(function (o) { o.x -= move; });
    g.obs = g.obs.filter(function (o) { return o.x + o.s.w > -4; });
    g.gap -= move;
    if (g.gap <= 0) {
      var s = OBSTACLES[Math.floor(Math.random() * OBSTACLES.length)];
      g.obs.push({ x: W + 4, s: s });
      g.gap = 70 + Math.random() * 90 + g.speed * 16;
    }
    g.clouds.forEach(function (c) { c.x -= move * 0.2; if (c.x < -30) { c.x = W + 10; c.y = 8 + Math.random() * 16; } });
    g.dots.forEach(function (d) { d.x -= move; if (d.x < 0) d.x += W; });

    if (g.mode === "demo") {
      // Jump so the pig is at the top of its arc right over the obstacle.
      var o = nextObstacle();
      var ahead = o ? (o.x + o.s.w / 2) - (PIG_X + PIG.a.w / 2) : Infinity;
      if (ahead > 0 && ahead <= g.speed * (-JUMP / GRAVITY)) jump();
    }

    g.vy += GRAVITY * dt;
    g.y += g.vy * dt;
    if (g.y >= GROUND) { g.y = GROUND; g.vy = 0; }

    if (g.mode === "play") {
      g.score += move * 0.1;
      if (g.score > g.hi) g.hi = g.score;
    }

    if (hit()) {
      if (g.mode === "play") { g.mode = "over"; g.overAt = performance.now(); }
      else { window.__pigrun.demoCrashes++; reset(); }
    }
  }

  function hit() {
    var px = PIG_X + 3, pw = PIG.a.w - 6, py = g.y - PIG.a.h + 4, ph = PIG.a.h - 5;
    for (var i = 0; i < g.obs.length; i++) {
      var o = g.obs[i], ox = o.x + 2, ow = o.s.w - 4, oy = GROUND - o.s.h + 2, oh = o.s.h - 2;
      if (px < ox + ow && px + pw > ox && py < oy + oh && py + ph > oy) return true;
    }
    return false;
  }

  function text(str, x, y, size, align, color) {
    ctx.font = size + 'px "Pixelify Sans", monospace';
    ctx.textAlign = align;
    ctx.textBaseline = "alphabetic";
    ctx.fillStyle = color || COLORS.M;
    ctx.fillText(str, x, y);
  }

  function pad(n) { return ("00000" + Math.floor(n)).slice(-5); }

  function draw() {
    ctx.fillStyle = PAPER;
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = CLOUD;
    g.clouds.forEach(function (c) {
      var x = Math.round(c.x), y = Math.round(c.y);
      ctx.fillRect(x + 4, y, 12, 2); ctx.fillRect(x, y + 2, 22, 3);
    });

    ctx.fillStyle = LINE;
    ctx.fillRect(0, GROUND, W, 1);
    g.dots.forEach(function (d) { ctx.fillRect(Math.round(d.x), d.y, 2, 1); });

    g.obs.forEach(function (o) {
      ctx.drawImage(o.s.img, Math.round(o.x), GROUND - o.s.h + 1);
    });

    var frame = g.y < GROUND ? PIG.up : (Math.floor(g.run / 7) % 2 ? PIG.b : PIG.a);
    if (g.mode === "still") frame = PIG.a;
    ctx.drawImage(frame.img, PIG_X, Math.round(g.y) - frame.h + 1);

    if (g.mode === "play" || g.mode === "over") {
      text("HI " + pad(g.hi) + "  " + pad(g.score), W - 4, 9, 7, "right");
    }
    if (g.mode === "demo" || g.mode === "still") {
      text("Click or tap to play", W / 2, 22, 8, "center");
    }
    if (g.mode === "over") {
      text("Oink! You woke up.", W / 2, 20, 9, "center");
      text("Click, tap or press Space to go again", W / 2, 31, 6, "center", "#000");
    }
  }

  var last = 0, visible = true, raf = 0;
  function frame(t) {
    raf = 0;
    var dt = last ? Math.min(3, (t - last) / 16.667) : 1;
    last = t;
    if (g.mode === "demo" || g.mode === "play") step(dt);
    if (g.mode === "over" && performance.now() - g.overAt > 8000 && !reduced) { g.mode = "demo"; reset(); }
    draw();
    loop();
  }
  function loop() {
    if (!raf && visible && !document.hidden && g.mode !== "still") raf = requestAnimationFrame(frame);
    else if (!raf) last = 0;
  }

  function act(e) {
    if (g.mode === "play") { jump(); }
    else {
      g.mode = "play"; reset(); jump();
    }
    if (e) e.preventDefault();
    loop();
  }
  canvas.addEventListener("pointerdown", function (e) { canvas.focus({ preventScroll: true }); act(e); });
  canvas.addEventListener("keydown", function (e) {
    if (e.key === " " || e.key === "ArrowUp" || e.key === "Enter") act(e);
  });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      loop();
    }).observe(canvas);
  }
  document.addEventListener("visibilitychange", loop);
  if ("ResizeObserver" in window) new ResizeObserver(size).observe(box);
  else window.addEventListener("resize", size);

  reset();
  size();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
  loop();
})();
