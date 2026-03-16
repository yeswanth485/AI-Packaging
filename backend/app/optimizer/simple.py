from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Item:
    sku: str
    qty: int
    length: float
    width: float
    height: float
    weight: float = 0.0

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height

    @property
    def dims_sorted(self) -> Tuple[float, float, float]:
        return tuple(sorted((self.length, self.width, self.height)))


@dataclass(frozen=True)
class BoxType:
    code: str
    inner_length: float
    inner_width: float
    inner_height: float
    max_weight: float = 0.0  # 0 means "ignore"

    @property
    def volume(self) -> float:
        return self.inner_length * self.inner_width * self.inner_height

    @property
    def dims_sorted(self) -> Tuple[float, float, float]:
        return tuple(sorted((self.inner_length, self.inner_width, self.inner_height)))


def _fits_by_dimensions(item: Item, box: BoxType) -> bool:
    il, iw, ih = item.dims_sorted
    bl, bw, bh = box.dims_sorted
    return il <= bl and iw <= bw and ih <= bh


@dataclass
class PackedItem:
    sku: str
    length: float
    width: float
    height: float
    weight: float

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height


@dataclass
class PackedBox:
    box_code: str
    inner_length: float
    inner_width: float
    inner_height: float
    items: List[PackedItem]

    @property
    def capacity_volume(self) -> float:
        return self.inner_length * self.inner_width * self.inner_height

    @property
    def used_volume(self) -> float:
        return sum(i.volume for i in self.items)

    @property
    def used_weight(self) -> float:
        return sum(i.weight for i in self.items)


def _choose_smallest_box_that_can_fit(
    item: Item, box_types: Iterable[BoxType]
) -> Optional[BoxType]:
    candidates = [b for b in box_types if _fits_by_dimensions(item, b)]
    if not candidates:
        return None
    return min(candidates, key=lambda b: b.volume)


def pack_first_fit_by_volume(
    items: List[Item],
    box_types: List[BoxType],
) -> Tuple[List[PackedBox], List[str]]:
    """
    Very first working heuristic:
    - Expands qty into single units
    - Sorts units by volume (largest first)
    - First-Fit into an existing box if:
        - item dims fit the box (rotation allowed via sorted dims)
        - total used volume stays <= box volume
        - (optional) total weight stays <= max_weight when max_weight > 0
      Otherwise opens a new box (smallest possible that can fit the item)

    Limitations (intentional for v1):
    - Uses volume as a proxy for spatial packing (no exact 3D placement yet)
    """
    if not box_types:
        return [], ["No box types provided"]

    # Normalize and expand units
    units: List[Item] = []
    for it in items:
        if it.qty <= 0:
            continue
        for _ in range(it.qty):
            units.append(Item(sku=it.sku, qty=1, length=it.length, width=it.width, height=it.height, weight=it.weight))

    if not units:
        return [], []

    # Sort box types by volume asc for "smallest that fits"
    box_types_sorted = sorted(box_types, key=lambda b: b.volume)

    # Sort units by volume desc (place big stuff first)
    units.sort(key=lambda u: u.volume, reverse=True)

    packed: List[PackedBox] = []
    errors: List[str] = []

    for unit in units:
        placed = False

        for pb in packed:
            # Dimension fit always required
            box = BoxType(
                code=pb.box_code,
                inner_length=pb.inner_length,
                inner_width=pb.inner_width,
                inner_height=pb.inner_height,
                max_weight=0.0,
            )
            if not _fits_by_dimensions(unit, box):
                continue

            # Volume constraint
            if pb.used_volume + unit.volume > pb.capacity_volume:
                continue

            # No max weight check here because pb doesn't carry it yet (v1)
            pb.items.append(
                PackedItem(
                    sku=unit.sku,
                    length=unit.length,
                    width=unit.width,
                    height=unit.height,
                    weight=unit.weight,
                )
            )
            placed = True
            break

        if placed:
            continue

        # Need a new box
        chosen = _choose_smallest_box_that_can_fit(unit, box_types_sorted)
        if chosen is None:
            errors.append(f"Item '{unit.sku}' does not fit in any available box type")
            continue

        packed.append(
            PackedBox(
                box_code=chosen.code,
                inner_length=chosen.inner_length,
                inner_width=chosen.inner_width,
                inner_height=chosen.inner_height,
                items=[
                    PackedItem(
                        sku=unit.sku,
                        length=unit.length,
                        width=unit.width,
                        height=unit.height,
                        weight=unit.weight,
                    )
                ],
            )
        )

    return packed, errors

