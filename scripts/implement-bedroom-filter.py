from pathlib import Path


def replace(path_name: str, old: str, new: str, label: str) -> None:
    path = Path(path_name)
    source = path.read_text(encoding="utf-8")
    if old not in source:
        raise SystemExit(f"{path_name}: missing anchor: {label}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


replace(
    "src/types.ts",
    "  roomSizeM2: number\n  currentResidents: number\n",
    "  roomSizeM2: number\n  bedroomCount?: number\n  currentResidents: number\n",
    "Listing bedroomCount",
)
replace(
    "src/types.ts",
    "  roomSizeM2: number\n  currentResidents: number\n  roomCapacity: 1 | 2\n",
    "  roomSizeM2: number\n  bedroomCount: number\n  currentResidents: number\n  roomCapacity: 1 | 2\n",
    "ListingDraft bedroomCount",
)

replace(
    "src/data/listings.ts",
    "  const roomCapacity: Listing['roomCapacity'] = tenantRequirement === 'couple' || (tenantRequirement === 'any' && index % 4 === 1) ? 2 : 1\n",
    "  const roomCapacity: Listing['roomCapacity'] = tenantRequirement === 'couple' || (tenantRequirement === 'any' && index % 4 === 1) ? 2 : 1\n  const bedroomCount = index % 9 === 5 ? 1 : 1 + (index % 12)\n",
    "seed bedroomCount constant",
)
replace(
    "src/data/listings.ts",
    "    roomSizeM2: 9 + (index % 10),\n    currentResidents: 1 + (index % 6),\n",
    "    roomSizeM2: 9 + (index % 10),\n    bedroomCount,\n    currentResidents: 1 + (index % 6),\n",
    "seed bedroomCount property",
)
replace(
    "src/data/listings.ts",
    "    homeDescription: `Vivienda de ${2 + (index % 4)} dormitorios con zonas comunes equipadas. La posición del mapa es aproximada para proteger la privacidad.`,\n",
    "    homeDescription: `Vivienda de ${bedroomCount} ${bedroomCount === 1 ? 'dormitorio' : 'dormitorios'} con zonas comunes equipadas. La posición del mapa es aproximada para proteger la privacidad.`,\n",
    "aligned seed home description",
)
replace(
    "src/data/listings.ts",
    "roomType: 'Habitación individual', roomSizeM2: 12, currentResidents: 4, roomCapacity: 1,",
    "roomType: 'Habitación individual', roomSizeM2: 12, bedroomCount: 4, currentResidents: 4, roomCapacity: 1,",
    "default draft bedroomCount",
)

replace(
    "src/lib/listings.ts",
    "export function getPrimaryCadence(listing: Listing): 'mes' | 'noche' {\n  return listing.rentalMode === 'holiday' ? 'noche' : 'mes'\n}\n",
    "export function getPrimaryCadence(listing: Listing): 'mes' | 'noche' {\n  return listing.rentalMode === 'holiday' ? 'noche' : 'mes'\n}\n\nexport function getBedroomCount(listing: Listing) {\n  const explicit = Number(listing.bedroomCount)\n  if (Number.isFinite(explicit) && explicit >= 1) return Math.min(99, Math.max(1, Math.round(explicit)))\n  if (listing.roomType === 'Estudio') return 1\n  return Math.min(99, Math.max(1, Math.round((listing.currentResidents || 1) + 1)))\n}\n",
    "getBedroomCount helper",
)
replace(
    "src/lib/listings.ts",
    "    roomSizeM2: typeof legacy.roomSizeM2 === 'number' ? legacy.roomSizeM2 : typeof legacy.size === 'number' ? legacy.size : 12,\n    currentResidents: typeof legacy.currentResidents === 'number' ? legacy.currentResidents : typeof legacy.occupants === 'number' ? legacy.occupants : 1,\n",
    "    roomSizeM2: typeof legacy.roomSizeM2 === 'number' ? legacy.roomSizeM2 : typeof legacy.size === 'number' ? legacy.size : 12,\n    bedroomCount: typeof legacy.bedroomCount === 'number' && Number.isFinite(legacy.bedroomCount)\n      ? Math.min(99, Math.max(1, Math.round(legacy.bedroomCount)))\n      : legacy.roomType === 'Estudio' ? 1 : Math.min(99, Math.max(1, Math.round((legacy.currentResidents ?? legacy.occupants ?? 1) + 1))),\n    currentResidents: typeof legacy.currentResidents === 'number' ? legacy.currentResidents : typeof legacy.occupants === 'number' ? legacy.occupants : 1,\n",
    "normalize bedroomCount",
)

replace(
    "src/pages/PublishPage.tsx",
    "  roomSizeM2: listing.roomSizeM2,\n  currentResidents: listing.currentResidents,\n",
    "  roomSizeM2: listing.roomSizeM2,\n  bedroomCount: listing.bedroomCount ?? (listing.roomType === 'Estudio' ? 1 : Math.max(1, listing.currentResidents + 1)),\n  currentResidents: listing.currentResidents,\n",
    "toDraft bedroomCount",
)
replace(
    "src/pages/PublishPage.tsx",
    "    roomSizeM2: draft.roomSizeM2,\n    currentResidents: draft.currentResidents,\n",
    "    roomSizeM2: draft.roomSizeM2,\n    bedroomCount: Math.min(99, Math.max(1, Math.round(draft.bedroomCount))),\n    currentResidents: draft.currentResidents,\n",
    "toListing bedroomCount",
)
replace(
    "src/pages/PublishPage.tsx",
    "    if (step === 2 && draft.currentResidents < 0)\n      next.currentResidents = \"El número de residentes no puede ser negativo.\";\n",
    "    if (step === 2 && (draft.bedroomCount < 1 || draft.bedroomCount > 99))\n      next.bedroomCount = \"Indica entre 1 y 99 habitaciones.\";\n    if (step === 2 && draft.currentResidents < 0)\n      next.currentResidents = \"El número de residentes no puede ser negativo.\";\n",
    "bedroomCount validation",
)
replace(
    "src/pages/PublishPage.tsx",
    """              <FormField
                label=\"Personas que viven en casa\"
                htmlFor=\"publish-residents\"
                error={errors.currentResidents}
              >""",
    """              <FormField
                label=\"Número de habitaciones de la vivienda\"
                htmlFor=\"publish-bedrooms\"
                error={errors.bedroomCount}
              >
                <Input
                  id=\"publish-bedrooms\"
                  type=\"number\"
                  min=\"1\"
                  max=\"99\"
                  value={draft.bedroomCount}
                  aria-invalid={Boolean(errors.bedroomCount)}
                  aria-describedby={errors.bedroomCount ? \"publish-bedrooms-error\" : undefined}
                  onChange={(e) => set(\"bedroomCount\", Math.min(99, Math.max(1, Number(e.target.value) || 1)))}
                />
              </FormField>
              <FormField
                label=\"Personas que viven en casa\"
                htmlFor=\"publish-residents\"
                error={errors.currentResidents}
              >""",
    "publication bedroom count field",
)

replace(
    "src/lib/mobile-search.ts",
    "import { filterListings, pointInPolygon, sortListings } from '@/lib/search'\n",
    "import { getBedroomCount } from '@/lib/listings'\nimport { filterListings, pointInPolygon, sortListings } from '@/lib/search'\n",
    "mobile search bedroom helper import",
)
replace(
    "src/lib/mobile-search.ts",
    "  const capacities = (params.get('capacidades') ?? '').split('|').filter(Boolean).map(Number).filter(Number.isFinite)\n",
    "  const bedroomFilters = (params.get('habitaciones') ?? '').split('|').filter(Boolean)\n  const exactBedroomCounts = bedroomFilters.map(Number).filter((value) => Number.isInteger(value) && value >= 1 && value <= 10)\n  const moreThanTenBedrooms = bedroomFilters.includes('10+')\n",
    "mobile bedroom params",
)
replace(
    "src/lib/mobile-search.ts",
    "    if (capacities.length && !capacities.includes(listing.roomCapacity)) return false\n",
    "    const bedroomCount = getBedroomCount(listing)\n    if (bedroomFilters.length && !exactBedroomCounts.includes(bedroomCount) && !(moreThanTenBedrooms && bedroomCount > 10)) return false\n",
    "mobile bedroom filter predicate",
)

replace(
    "src/components/mobile-search-results.tsx",
    "import { defaultFilters } from '@/data/listings'\n",
    "import { defaultFilters } from '@/data/listings'\nimport { getBedroomCount } from '@/lib/listings'\n",
    "results bedroom helper import",
)
replace(
    "src/components/mobile-search-results.tsx",
    "type ResultsPanel = 'results' | 'filters' | 'sort'\n",
    "type ResultsPanel = 'results' | 'filters' | 'sort'\ntype ExactRoomCount = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10\ntype RoomCountFilter = ExactRoomCount | '10+'\nconst roomCountOptions: readonly RoomCountFilter[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, '10+']\n",
    "room count filter types",
)
replace(
    "src/components/mobile-search-results.tsx",
    "  roomCounts: number[]\n",
    "  roomCounts: RoomCountFilter[]\n",
    "typed roomCounts",
)
replace(
    "src/components/mobile-search-results.tsx",
    "    vivienda: 'Vivienda', turismo: 'Turismo', price: 'Precio', area: 'Superficie', min: 'Mín', max: 'Máx', housingType: 'Tipo de vivienda', rooms: 'Número de habitaciones', oneRoom: '1 habitación', twoRooms: '2 habitaciones',\n",
    "    vivienda: 'Vivienda', turismo: 'Turismo', price: 'Precio', area: 'Superficie', min: 'Mín', max: 'Máx', housingType: 'Tipo de vivienda', rooms: 'Número de habitaciones', roomCount: (count: number) => `${count} ${count === 1 ? 'habitación' : 'habitaciones'}`, moreThanTenRooms: 'Más de 10 habitaciones',\n",
    "Spanish room labels",
)
replace(
    "src/components/mobile-search-results.tsx",
    "    vivienda: 'Housing', turismo: 'Tourism', price: 'Price', area: 'Area', min: 'Min', max: 'Max', housingType: 'Property category', rooms: 'Number of rooms', oneRoom: '1 room', twoRooms: '2 rooms',\n",
    "    vivienda: 'Housing', turismo: 'Tourism', price: 'Price', area: 'Area', min: 'Min', max: 'Max', housingType: 'Property category', rooms: 'Number of rooms', roomCount: (count: number) => `${count} ${count === 1 ? 'room' : 'rooms'}`, moreThanTenRooms: 'More than 10 rooms',\n",
    "English room labels",
)
replace(
    "src/components/mobile-search-results.tsx",
    "    vivienda: 'Жильё', turismo: 'Туризм', price: 'Цена', area: 'Площадь', min: 'Мин', max: 'Макс', housingType: 'Тип жилья', rooms: 'Количество комнат', oneRoom: '1 комната', twoRooms: '2 комнаты',\n",
    "    vivienda: 'Жильё', turismo: 'Туризм', price: 'Цена', area: 'Площадь', min: 'Мин', max: 'Макс', housingType: 'Тип жилья', rooms: 'Количество комнат', roomCount: (count: number) => `${count} ${count === 1 ? 'комната' : count >= 2 && count <= 4 ? 'комнаты' : 'комнат'}`, moreThanTenRooms: 'Больше 10 комнат',\n",
    "Russian room labels",
)
replace(
    "src/components/mobile-search-results.tsx",
    """function capacityLabel(language: ResultsLanguage, count: number) {
  if (language === 'ru') return `Комната для ${count} ${count === 1 ? 'человека' : 'человек'}`
  if (language === 'en') return `Room for ${count} ${count === 1 ? 'person' : 'people'}`
  return `Habitación para ${count} ${count === 1 ? 'persona' : 'personas'}`
}
""",
    """function capacityLabel(language: ResultsLanguage, count: number) {
  if (language === 'ru') return `Комната для ${count} ${count === 1 ? 'человека' : 'человек'}`
  if (language === 'en') return `Room for ${count} ${count === 1 ? 'person' : 'people'}`
  return `Habitación para ${count} ${count === 1 ? 'persona' : 'personas'}`
}

function bedroomFact(language: ResultsLanguage, count: number) {
  if (language === 'ru') return `${count} ${count === 1 ? 'комната' : count >= 2 && count <= 4 ? 'комнаты' : 'комнат'}`
  if (language === 'en') return `${count} ${count === 1 ? 'room' : 'rooms'}`
  return `${count} ${count === 1 ? 'habitación' : 'habitaciones'}`
}
""",
    "bedroom fact helper",
)
replace(
    "src/components/mobile-search-results.tsx",
    '<p className="m2-result-card__facts">{listing.roomType} · {listing.roomSizeM2} m² · {listing.currentResidents} {t.residents}</p>',
    '<p className="m2-result-card__facts">{listing.roomType} · {bedroomFact(language, getBedroomCount(listing))} · {listing.roomSizeM2} m² · {listing.currentResidents} {t.residents}</p>',
    "result card bedroom fact",
)
replace(
    "src/components/mobile-search-results.tsx",
    "    const roomCounts = (params.get('capacidades') ?? '').split('|').map(Number).filter((value): value is 1 | 2 => value === 1 || value === 2)\n",
    "    const roomCounts = (params.get('habitaciones') ?? '').split('|').map((value): RoomCountFilter | null => {\n      if (value === '10+') return value\n      const count = Number(value)\n      return Number.isInteger(count) && count >= 1 && count <= 10 ? count as ExactRoomCount : null\n    }).filter((value): value is RoomCountFilter => value !== null)\n",
    "parse room count filters",
)
for label in ("live bedroom URL params", "applied bedroom URL params"):
    replace(
        "src/components/mobile-search-results.tsx",
        "    if (filters.roomCounts.length) params.set('capacidades', filters.roomCounts.join('|'))\n    else params.delete('capacidades')\n",
        "    params.delete('capacidades')\n    if (filters.roomCounts.length) params.set('habitaciones', filters.roomCounts.join('|'))\n    else params.delete('habitaciones')\n",
        label,
    )
replace(
    "src/components/mobile-search-results.tsx",
    """      <fieldset><legend>{t.rooms}</legend><div className="m2-results-filter__checks">{[[1, t.oneRoom], [2, t.twoRooms]].map(([value, label]) => <label key={String(value)}><input type="checkbox" checked={filters.roomCounts.includes(value as number)} onChange={() => setFilters((current) => ({ ...current, roomCounts: toggleValue(current.roomCounts, value as number) }))} /><span>{label}</span></label>)}</div></fieldset>""",
    """      <fieldset><legend>{t.rooms}</legend><div className="m2-results-filter__checks m2-results-filter__checks--rooms">{roomCountOptions.map((value) => { const label = value === '10+' ? t.moreThanTenRooms : t.roomCount(value); return <label key={String(value)}><input type="checkbox" checked={filters.roomCounts.includes(value)} onChange={() => setFilters((current) => ({ ...current, roomCounts: toggleValue(current.roomCounts, value) }))} /><span>{label}</span></label> })}</div></fieldset>""",
    "room count checkbox UI",
)

css = Path("src/mobile-search-results.css")
source = css.read_text(encoding="utf-8")
marker = "/* Numeric filter focus and bedroom-count layout */"
if marker not in source:
    source += """

/* Numeric filter focus and bedroom-count layout */
.m2-results-filter__pair > label {
  position: relative;
  transition: border-color .12s ease, box-shadow .12s ease;
}

.m2-results-filter__pair > label:focus-within {
  border-color: #00858d !important;
  box-shadow: 0 0 0 3px rgb(0 133 141 / .72) !important;
}

.m2-results-filter__pair input:focus,
.m2-results-filter__pair input:focus-visible {
  outline: none !important;
  outline-offset: 0 !important;
  box-shadow: none !important;
}

.m2-results-filter__checks--rooms {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0;
}

.m2-results-filter__checks--rooms > label {
  min-width: 0;
}

.m2-results-filter__checks--rooms > label:last-child {
  grid-column: 1 / -1;
}
"""
    css.write_text(source, encoding="utf-8")

print("Bedroom filter implementation applied.")
