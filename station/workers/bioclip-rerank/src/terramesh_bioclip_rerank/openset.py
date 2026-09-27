"""Two checks before a name is suggested, because a softmax over species has no "no organism"
answer: shown bark mulch or a flower pot, BioCLIP still names its likeliest species, often an
animal, with a high score. On Dan's 17 Sep Elkhorn walk it called mulch a West Coast lady (0.94)
and straw a California kingsnake (0.79).

1. Background. The photograph is compared with plain descriptions of what a tapped crop often
   really shows (ground, mulch, stones, pots, fences). If one of those matches better than every
   species, no name is suggested.
2. Kingdom. The phone's scene model already described each crop (`sceneDescription
   .semanticIdentifier`). A top species from another kingdom than a plant or animal label the
   phone saw is not suggested. This is the kingdom half of `SemanticTaxonomyAgreementResult.assess`
   in TerraMeshCore. Its family hints ("grass" means Poaceae, "tree" means a few tree families)
   are reported but never withhold a name here: on the Elkhorn walk they withheld four clear
   sycamore trunks and three prickly pear pads that the phone's scene model had called grass.
   BioCLIP 2.5 knows a family better than a 1,300-label scene model does; a kingdom it does not.

Either way the candidates stay in the layer for a person to review; only the suggestion is withheld.

A name that nothing on the phone supports (no plant, animal or fungus scene label that agrees) is
still suggested but flagged for review. An earlier version flagged only when a background description
came within 0.03; that caught a kingsnake on straw with a 969-species cube and missed a racer on the
same straw with the 43,197-species California cube, where every photograph finds a closer species.
"""
from __future__ import annotations
BACKGROUND_VERSION = 1

def background_prompts() -> list[list[str]]:
    ...

def kingdom_agreement(semantic_identifier: str, taxon: dict) -> str:
    """"agree", "conflict", "unknown" or "notApplicable" for one scene label and one species: the
    kingdom rule of the phone's `assess`, without its family hints (see `family_hint`)."""
    ...

def family_hint(semantic_identifier: str, taxon: dict) -> str | None:
    """Whether the species is in the family a narrow scene label implies ("same" or "differs"), or
    None when the label implies none. Advisory only: the phone's `assess` would call "differs" a
    conflict."""
    ...

def kingdom_verdict(scene_labels: list[str], taxon: dict) -> tuple[str, str | None]:
    """Across an observation's photographs: any photograph whose label agrees supports the name;
    otherwise any conflict withholds it. Returns the verdict and the label that decided it."""
    ...
