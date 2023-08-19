% load Phenesthe
:-['../../phenesthe.prolog'].
% load the maritime definitions
:-['./definitions.pl'].
% sensor activity thresholds
:-['./thresholds.pl'].
% preprocess phenomena definitions (transform them, find evaluation order, etc.)
:-preprocess_phenomena_definitions.