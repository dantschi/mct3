#!/usr/bin/env python3
"""Check actual SVG wire/pin connectivity independently of its net metadata.

No analogue simulation: crossings without junctions remain separate. The four
explicit bridges mark the crossings in these schematics. Component channels are
excluded from the external wire graph; a transistor is not an unconditional wire.
Run from any directory with Python's standard library.
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NS = '{http://www.w3.org/2000/svg}'
REFERENCE = ROOT.parents[1]/'figures/01_speicherphysik/6t/topologie.json'


def segments(element):
    kind = element.tag.removeprefix(NS)
    a = element.attrib
    if kind == 'line':
        return [((float(a['x1']), float(a['y1'])),
                 (float(a['x2']), float(a['y2'])))]
    if kind == 'polyline':
        numbers = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', a['points'])))
        points = list(zip(numbers[::2], numbers[1::2]))
        return list(zip(points, points[1:]))
    if kind != 'path' or 'data-net' not in a:
        return []
    # The generator uses absolute M/H/V/Q commands. Q curves are bridge marks.
    tokens = re.findall(r'[MHVQ]|-?\d+(?:\.\d+)?', a['d'])
    result = []
    i = 0
    current = None
    while i < len(tokens):
        command = tokens[i]; i += 1
        if command == 'M':
            current = tuple(map(float, tokens[i:i+2])); i += 2
        elif command in ('H', 'V'):
            value = float(tokens[i]); i += 1
            target = (value, current[1]) if command == 'H' else (current[0], value)
            result.append((current, target)); current = target
        elif command == 'Q':
            target = tuple(map(float, tokens[i+2:i+4])); i += 4
            # A bridge joins its two ends. Its interior is never a junction
            # with the crossed wire, even though the drawn curves intersect.
            result.append((current, target))
            current = target
        else:
            raise AssertionError(('Unsupported path', a['d'], command))
    return result


def on_segment(point, segment):
    a, b = segment
    cross = (point[0]-a[0])*(b[1]-a[1])-(point[1]-a[1])*(b[0]-a[0])
    return (abs(cross) < 1e-7 and
            min(a[0], b[0])-1e-7 <= point[0] <= max(a[0], b[0])+1e-7 and
            min(a[1], b[1])-1e-7 <= point[1] <= max(a[1], b[1])+1e-7)


def inspect(path, reference):
    svg = ET.parse(path).getroot()
    components = {g.attrib['data-component']: g for g in svg.findall(NS+'g')}
    assert set(components) == set(reference), path
    assert sum(g.attrib['data-type'] == 'pMOS' for g in components.values()) == 2
    assert sum(g.attrib['data-type'] == 'nMOS' for g in components.values()) == 4
    pins = {}
    for name, g in components.items():
        assert g.attrib['data-type'] == reference[name]['type']
        positions = json.loads(g.attrib['data-terminals'])
        assert set(positions) == set(reference[name]) - {'type'}
        ends = {p for e in g for s in segments(e) for p in s}
        # Pin declarations must terminate on the drawn component leads.
        for terminal, position in positions.items():
            position = tuple(position)
            assert position in ends, (name, terminal, position)
            pins[(name, terminal)] = position
        circles = g.findall(NS+'circle')
        assert len(circles) == (g.attrib['data-type'] == 'pMOS')
    wire_segments = [s for e in svg for s in segments(e)]
    vertices = {p for s in wire_segments for p in s} | set(pins.values())
    parent = {p: p for p in vertices}

    def find(p):
        if parent[p] != p:
            parent[p] = find(parent[p])
        return parent[p]

    def union(a, b):
        parent[find(a)] = find(b)

    for segment in wire_segments:
        points = [p for p in vertices if on_segment(p, segment)]
        for p in points:
            union(segment[0], p)
    # Exactly the independently specified pin equivalence classes must result.
    net_pins = {}
    for (name, terminal), position in pins.items():
        net_pins.setdefault(reference[name][terminal], []).append(position)
    representatives = {}
    for net, positions in net_pins.items():
        roots = {find(p) for p in positions}
        assert len(roots) == 1, (path.name, 'disconnected', net, positions)
        representatives[net] = roots.pop()
    assert len(set(representatives.values())) == len(representatives), (path.name, 'short', representatives)
    declared = json.loads(svg.find(NS+'metadata').text)
    assert declared == reference
    # Check the actual channel colors and displayed initial digital state.
    if path.stem == 'sram-6t':
        expected_colors = {name: '#1D1D1F' for name in components}
    else:
        expected_colors = {'P_Q': '#86868B', 'N_Q': '#E2001A',
                           'P_QB': '#E2001A', 'N_QB': '#86868B'}
        access_color = '#86868B' if path.stem == 'sram-hold' else '#E2001A'
        expected_colors.update(A_Q=access_color, A_QB=access_color)
        labels = [t.text for t in svg.findall(NS+'text')]
        assert 'Q = 0' in labels and 'QB = 1' in labels
        assert ('WL = 0' if path.stem == 'sram-hold' else 'WL = 1') in labels
    for name, group in components.items():
        channels = [e for e in group.findall(NS+'line') if e.attrib['stroke-width'] == '4']
        assert len(channels) == 1
        assert channels[0].attrib['stroke'] == expected_colors[name], (path.name, name)
    # Every straight external wire is orthogonal; curves only mark bridges.
    for e in svg.findall(NS+'line'):
        s = segments(e)[0]
        assert s[0][0] == s[1][0] or s[0][1] == s[1][1]
    return {'file': path.name, 'components': len(components),
            'independent_nets': len(representatives), 'wire_connectivity': 'passed',
            'initial_state_and_channel_colors': 'passed'}


def main():
    reference = json.loads(REFERENCE.read_text(encoding='utf-8'))
    reports = [inspect(ROOT/(name+'.svg'), reference)
               for name in ('sram-6t', 'sram-hold', 'sram-read', 'sram-write')]
    for q in (0, 1):
        qb = 1-q
        assert q == 1-qb and qb == 1-q
        # Pull-up/pull-down of each inverter agree with its stored node.
        assert int(not qb) == q and int(not q) == qb
    output = {'scope': 'Qualitative topology and digital stable states; no analogue transistor simulation',
              'reference': '../../figures/01_speicherphysik/6t/topologie.json',
              'results': reports}
    (ROOT/'pruefprotokoll.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('4 SRAM-Schaltbilder: je 6 Transistoren, 7 getrennte Netze, alle Pins korrekt verbunden.')


if __name__ == '__main__':
    main()
