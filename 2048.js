// 2048 apo to duckduck search result
!(function () {
    var n = Handlebars.template,
        e = (DDH.game2048 = DDH.game2048 || {});
    e.content = n(function (n, e, a, t, o) {
        function s(n, e) {
            var t,
                o,
                s,
                r = '';
            return (
                (r += '\n                <tr>'),
                (o = a.loop || (n && n.loop)),
                (s = { hash: {}, inverse: m.noop, fn: m.program(2, i, e), data: e }),
                (t = o ? o.call(n, 4, s) : _.call(n, 'loop', 4, s)),
                (t || 0 === t) && (r += t),
                (r += '</tr>\n            ')
            );
        }
        function i() {
            return '<td class="cell val-"></td>';
        }
        (this.compilerInfo = [4, '>= 1.0.0']), (a = this.merge(a, n.helpers)), (o = o || {});
        var r,
            l,
            d,
            c = '',
            m = this,
            _ = a.helperMissing;
        return (
            (c +=
                '<div class="game2048__container">\n\n\n    <div id="game2048__area_container">\n        <div class="game2048__message">\n            <p></p>\n        </div>\n        <table id="game2048__area" class ="game2048__area" tabindex="0">\n            '),
            (l = a.loop || (e && e.loop)),
            (d = { hash: {}, inverse: m.noop, fn: m.program(1, s, o), data: o }),
            (r = l ? l.call(e, 4, d) : _.call(e, 'loop', 4, d)),
            (r || 0 === r) && (c += r),
            (c +=
                '\n        </table>\n    </div>\n    \n    <div class="game2048__info">\n        <div class="game2048__counter">\n            <div class="game2048__points_addition"></div>\n            <div class="game2048__points">0</div>\n        </div>\n\n        <div class="game2048__help tx-clr--dark">\n            Use your <strong>arrow-keys</strong> to move the tiles. When two tiles with the same number touch, they <strong>merge into one</strong>!\n        </div>\n\n        <button class="game2048__new_game">New Game</button>\n    </div>\n\n</div>\n')
        );
    });
})();
DDH.game2048 = DDH.game2048 || {};
DDH.game2048.build = function (ops) {
    'use strict';
    if (DDG.device.isMobile || DDG.device.isMobileDevice) {
        return DDH.failed('game2048');
    }
    var WINNUM = 2048,
        SIZE = 4,
        TILE_COUNT = SIZE * SIZE,
        started = false,
        tiles = init_area(),
        $game_area,
        $game_area_container,
        $game_points,
        $game_points_addition,
        $result_msg,
        $result_box,
        score = 0;
    function rc_to_index(row, col) {
        return row * SIZE + col;
    }
    function index_to_rc(index) {
        return { row: Math.floor(index / SIZE), col: index % SIZE };
    }
    function move(dir) {
        var points = 0;
        var transposed = false;
        var swapped = false;
        if (dir === 'w' || dir === 's') {
            transpose_area();
            transposed = true;
        }
        if (dir === 'd' || dir === 's') {
            swap_cols_area();
            swapped = true;
        }
        var result = handle_move(transposed, swapped);
        if (dir === 'd' || dir === 's') swap_cols_area();
        if (dir === 'w' || dir === 's') transpose_area();
        if (result.points > 0) increase_points(result.points);
        return result.moved;
    }
    function handle_move(transposed, swapped) {
        var result = { moved: false, points: false };
        var moves = 0;
        for (var i = 0; i < TILE_COUNT; ++i) {
            var row = Math.floor(i / SIZE),
                col = i % SIZE;
            moves = col === 0 ? 0 : moves;
            if (tiles[i].val === 0) {
                ++moves;
                continue;
            }
            if (moves > 0) {
                var temp_tile = tiles[rc_to_index(row, col - moves)];
                temp_tile.val = 0;
                tiles[rc_to_index(row, col - moves)] = tiles[i];
                tiles[i] = temp_tile;
                result.moved = true;
            }
            for (var j = col + 1; j < SIZE; ++j) {
                var tile_a = tiles[rc_to_index(row, col - moves)];
                var tile_b = tiles[rc_to_index(row, j)];
                if (tile_b.val === 0) continue;
                if (tile_a.val === tile_b.val) {
                    merge(tile_a, tile_b, row, col - moves, transposed, swapped);
                    result.points = tile_a.val;
                    result.moved = true;
                }
                break;
            }
        }
        return result;
    }
    function gen_translate_string(row, col) {
        return 'translate(' + (col * 85 + 5) + 'px,' + (row * 85 + 5) + 'px)';
    }
    function merge(tile_a, tile_b, row, col, transposed, swapped) {
        tile_a.val += tile_b.val;
        tile_b.val = 0;
        if (swapped) col = SIZE - 1 - col;
        if (transposed) {
            var tmp = col;
            col = row;
            row = tmp;
        }
        var translate_string = gen_translate_string(row, col);
        tile_b.tile_div.css({
            '-ms-transform': translate_string,
            '-webkit-transform': translate_string,
            transform: translate_string,
            opacity: 0,
        });
        tile_b.tile_div.on(
            'transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd',
            function () {
                $(this).remove();
            }
        );
    }
    function increase_points(points) {
        score += points;
        var addition = $('<div>').addClass('score-addition').text(points);
        $game_points.text(score);
        $game_points_addition.html(addition);
    }
    function reset_points() {
        score = 0;
        $game_points.text(0);
    }
    function update_tiles() {
        for (var i = 0; i < TILE_COUNT; ++i) {
            var pos = index_to_rc(i);
            var tile = tiles[i];
            if ('undefined' !== typeof tile.tile_div && tile.val > 0) {
                var translate_string = gen_translate_string(pos.row, pos.col);
                tile.tile_div
                    .html(tile.val)
                    .addClass('boxtile val-' + tile.val)
                    .css({
                        '-ms-transform': translate_string,
                        '-webkit-transform': translate_string,
                        transform: translate_string,
                        display: 'block',
                    });
            }
        }
    }
    function init_area() {
        var tiles = [TILE_COUNT];
        for (var i = 0; i < TILE_COUNT; ++i) {
            tiles[i] = { val: 0 };
        }
        return tiles;
    }
    function swap_tiles(a, b) {
        var tmp = tiles[a];
        tiles[a] = tiles[b];
        tiles[b] = tmp;
    }
    function transpose_area() {
        for (var i = 0; i < TILE_COUNT; ++i) {
            var pos = index_to_rc(i);
            if (pos.col >= pos.row) continue;
            var index_to_swap = rc_to_index(pos.col, pos.row);
            swap_tiles(i, index_to_swap);
        }
    }
    function swap_cols_area() {
        for (var i = 0; i < TILE_COUNT; ++i) {
            var pos = index_to_rc(i);
            if (pos.col >= SIZE / 2) continue;
            var index_to_swap = rc_to_index(pos.row, SIZE - 1 - pos.col);
            swap_tiles(i, index_to_swap);
        }
    }
    function add_random_tile() {
        var unused_tiles = [];
        for (var i = 0; i < TILE_COUNT; ++i) {
            if (tiles[i].val === 0) {
                unused_tiles.push(i);
            }
        }
        var rand_tile = unused_tiles[Math.floor(Math.random() * unused_tiles.length)];
        var rand_val = Math.floor(Math.random() * 11) < 2 ? 4 : 2;
        tiles[rand_tile].tile_div = create_tile_div();
        tiles[rand_tile].val = rand_val;
    }
    function create_tile_div() {
        var tile_div = $('<div>').hide();
        $game_area_container.append(tile_div);
        return tile_div;
    }
    function has_won() {
        for (var i = 0; i < TILE_COUNT; ++i) {
            if (tiles[i].val === WINNUM) {
                game_over_message(true);
                return true;
            }
        }
        return false;
    }
    function has_lost() {
        for (var i = 0; i < TILE_COUNT; ++i) {
            if (tiles[i].val === 0) return false;
            var pos = index_to_rc(i);
            if (
                (pos.row !== 0 && tiles[i].val === tiles[i - SIZE].val) ||
                (pos.row !== SIZE - 1 && tiles[i].val === tiles[i + SIZE].val) ||
                (pos.col !== 0 && tiles[i].val === tiles[i - 1].val) ||
                (pos.col !== SIZE - 1 && tiles[i].val === tiles[i + 1].val)
            ) {
                return false;
            }
        }
        game_over_message(false);
        return true;
    }
    function is_game_over() {
        return has_won() || has_lost();
    }
    function game_over_message(game_won) {
        if (game_won) {
            $result_msg.text('You Won!');
            $result_box.addClass('game2048__won');
        } else {
            $result_msg.text('You Lost!');
            $result_box.removeClass('game2048__won');
        }
        $result_box.show();
    }
    function init_game() {
        reset_points();
        $result_box.hide();
        $game_area_container.children('.boxtile').remove();
        $game_area.focus();
        tiles = init_area();
        add_random_tile();
        update_tiles();
    }
    function handle_buttons(e) {
        e.preventDefault();
        var move_made = false;
        if (is_game_over()) return false;
        if (e.keyCode === 87 || e.keyCode === 38) {
            move_made = move('w');
        } else if (e.keyCode === 65 || e.keyCode === 37) {
            move_made = move('a');
        } else if (e.keyCode === 83 || e.keyCode === 40) {
            move_made = move('s');
        } else if (e.keyCode === 68 || e.keyCode === 39) {
            move_made = move('d');
        }
        if (move_made) {
            add_random_tile();
            update_tiles();
        }
        return false;
    }
    return {
        onShow: function () {
            if (started) return;
            started = true;
            $game_area = $('#game2048__area');
            $game_area_container = $('#game2048__area_container');
            $game_points = $('.game2048__points');
            $game_points_addition = $('.game2048__points_addition');
            $result_msg = $('#game2048__area_container .game2048__message p');
            $result_box = $('#game2048__area_container .game2048__message');
            var $new_game_button = $('.zci--game2048 .game2048__new_game');
            $game_area.keydown(handle_buttons);
            init_game();
            $new_game_button.on('click', function (e) {
                e.preventDefault();
                init_game();
            });
        },
    };
};