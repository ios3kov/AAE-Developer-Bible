# Pixels, color, alpha

## Pixel depth

Effect должен явно иметь policy для:
- 8 bpc;
- 16 bpc;
- 32 bpc float.

Нельзя считать, что float values лежат только в 0..1: HDR pipelines могут содержать значения выше 1 и ниже 0.

## Rowbytes

Итерировать строки через `rowbytes`, а не через `width * sizeof(pixel)` assumption.

## Alpha

Перед алгоритмом определить:
- straight или premultiplied assumptions;
- что делает эффект с RGB при alpha=0;
- как interpolation/filtering работает на краях transparency.

Fringing часто появляется не из-за «плохого blur», а из-за неверной alpha/color model.

## Color management

Не делать самодельные преобразования между spaces без необходимости. Если алгоритм зависит от color space, использовать поддержанные host facilities и фиксировать assumptions в spec.

## Golden images

Для color effect хранить:
- neutral gray ramp;
- saturated primaries/secondaries;
- HDR ramp;
- transparent colored edge;
- alpha gradient;
- checker/impulse image;
- wide-gamut test image.
