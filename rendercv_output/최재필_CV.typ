
#import "@preview/fontawesome:0.5.0": fa-icon

#let name = "최재필"
#let locale-catalog-page-numbering-style = context { "최재필 - 페이지 " + str(here().page()) + " / " + str(counter(page).final().first()) + "" }
#let locale-catalog-last-updated-date-style = "최종 업데이트: 2025년 9월"
#let locale-catalog-language = "ko"
#let design-page-size = "us-letter"
#let design-section-titles-font-size = 1.2em
#let design-colors-text = rgb(0, 0, 0)
#let design-colors-section-titles = rgb(0, 0, 0)
#let design-colors-last-updated-date-and-page-numbering = rgb(128, 128, 128)
#let design-colors-name = rgb(0, 0, 0)
#let design-colors-connections = rgb(0, 0, 0)
#let design-colors-links = rgb(0, 0, 0)
#let design-section-titles-font-family = "Noto Sans"
#let design-section-titles-bold = true
#let design-section-titles-line-thickness = 0.5pt
#let design-section-titles-font-size = 1.2em
#let design-section-titles-type = "with-parial-line"
#let design-section-titles-vertical-space-above = 0.55cm
#let design-section-titles-vertical-space-below = 0.3cm
#let design-section-titles-small-caps = false
#let design-links-use-external-link-icon = false
#let design-text-font-size = 10pt
#let design-text-leading = 0.6em
#let design-text-font-family = "Noto Sans"
#let design-text-alignment = "left"
#let design-text-date-and-location-column-alignment = right
#let design-header-photo-width = 3.5cm
#let design-header-use-icons-for-connections = false
#let design-header-name-font-family = "Noto Sans"
#let design-header-name-font-size = 25pt
#let design-header-name-bold = false
#let design-header-connections-font-family = "Noto Sans"
#let design-header-vertical-space-between-name-and-connections = 0.7cm
#let design-header-vertical-space-between-connections-and-first-section = 0.7cm
#let design-header-use-icons-for-connections = false
#let design-header-horizontal-space-between-connections = 0.5cm
#let design-header-separator-between-connections = "|"
#let design-header-alignment = center
#let design-highlights-summary-left-margin = 0cm
#let design-highlights-bullet = "•"
#let design-highlights-top-margin = 0.25cm
#let design-highlights-left-margin = 0cm
#let design-highlights-vertical-space-between-highlights = 0.19cm
#let design-highlights-horizontal-space-between-bullet-and-highlights = 0.3em
#let design-entries-vertical-space-between-entries = 0.4cm
#let design-entries-date-and-location-width = 4.15cm
#let design-entries-allow-page-break-in-entries = true
#let design-entries-horizontal-space-between-columns = 0.1cm
#let design-entries-left-and-right-margin = 0cm
#let design-page-top-margin = 1cm
#let design-page-bottom-margin = 1cm
#let design-page-left-margin = 1cm
#let design-page-right-margin = 1cm
#let design-page-show-last-updated-date = true
#let design-page-show-page-numbering = false
#let design-links-underline = true
#let design-entry-types-education-entry-degree-column-width = 1cm
#let date = datetime.today()

// Metadata:
#set document(author: name, title: name + "'s CV", date: date)

// Page settings:
#set page(
  margin: (
    top: design-page-top-margin,
    bottom: design-page-bottom-margin,
    left: design-page-left-margin,
    right: design-page-right-margin,
  ),
  paper: design-page-size,
  footer: if design-page-show-page-numbering {
    text(
      fill: design-colors-last-updated-date-and-page-numbering,
      align(center, [_#locale-catalog-page-numbering-style _]),
      size: 0.9em,
    )
  } else {
    none
  },
  footer-descent: 0% - 0.3em + design-page-bottom-margin / 2,
)
// Text settings:
#let justify
#let hyphenate
#if design-text-alignment == "justified" {
  justify = true
  hyphenate = true
} else if design-text-alignment == "left" {
  justify = false
  hyphenate = false
} else if design-text-alignment == "justified-with-no-hyphenation" {
  justify = true
  hyphenate = false
}
#set text(
  font: design-text-font-family,
  size: design-text-font-size,
  lang: locale-catalog-language,
  hyphenate: hyphenate,
  fill: design-colors-text,
  // Disable ligatures for better ATS compatibility:
  ligatures: true,
)
#set par(
  spacing: 0pt,
  leading: design-text-leading,
  justify: justify,
)
#set enum(
  spacing: design-entries-vertical-space-between-entries,
)

// Highlights settings:
#let highlights(..content) = {
  list(
    ..content,
    marker: design-highlights-bullet,
    spacing: design-highlights-vertical-space-between-highlights,
    indent: design-highlights-left-margin,
    body-indent: design-highlights-horizontal-space-between-bullet-and-highlights,
  )
}
#show list: set list(
  marker: design-highlights-bullet,
  spacing: 0pt,
  indent: 0pt,
  body-indent: design-highlights-horizontal-space-between-bullet-and-highlights,
)

// Entry utilities:
#let three-col(
  left-column-width: 1fr,
  middle-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  middle-content: "",
  right-content: "",
  alignments: (auto, auto, auto),
) = [
  #block(
    grid(
      columns: (left-column-width, middle-column-width, right-column-width),
      column-gutter: design-entries-horizontal-space-between-columns,
      align: alignments,
      ([#set par(spacing: design-text-leading); #left-content]),
      ([#set par(spacing: design-text-leading); #middle-content]),
      ([#set par(spacing: design-text-leading); #right-content]),
    ),
    breakable: true,
    width: 100%,
  )
]

#let two-col(
  left-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  right-content: "",
  alignments: (auto, auto),
  column-gutter: design-entries-horizontal-space-between-columns,
) = [
  #block(
    grid(
      columns: (left-column-width, right-column-width),
      column-gutter: column-gutter,
      align: alignments,
      ([#set par(spacing: design-text-leading); #left-content]),
      ([#set par(spacing: design-text-leading); #right-content]),
    ),
    breakable: true,
    width: 100%,
  )
]

// Main heading settings:
#let header-font-weight
#if design-header-name-bold {
  header-font-weight = 700
} else {
  header-font-weight = 400
}
#show heading.where(level: 1): it => [
  #set par(spacing: 0pt)
  #set align(design-header-alignment)
  #set text(
    font: design-header-name-font-family,
    weight: header-font-weight,
    size: design-header-name-font-size,
    fill: design-colors-name,
  )
  #it.body
  // Vertical space after the name
  #v(design-header-vertical-space-between-name-and-connections)
]

#let section-title-font-weight
#if design-section-titles-bold {
  section-title-font-weight = 700
} else {
  section-title-font-weight = 400
}

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: (1em / 1.2)) // reset
  #set text(
    font: design-section-titles-font-family,
    size: (design-section-titles-font-size),
    weight: section-title-font-weight,
    fill: design-colors-section-titles,
  )
  #let section-title = (
    if design-section-titles-small-caps [
      #smallcaps(it.body)
    ] else [
      #it.body
    ]
  )
  // Vertical space above the section title
  #v(design-section-titles-vertical-space-above, weak: true)
  #block(
    breakable: false,
    width: 100%,
    [
      #if design-section-titles-type == "moderncv" [
        #two-col(
          alignments: (right, left),
          left-column-width: design-entries-date-and-location-width,
          right-column-width: 1fr,
          left-content: [
            #align(horizon, box(width: 1fr, height: design-section-titles-line-thickness, fill: design-colors-section-titles))
          ],
          right-content: [
            #section-title
          ]
        )

      ] else [
        #box(
          [
            #section-title
            #if design-section-titles-type == "with-parial-line" [
              #box(width: 1fr, height: design-section-titles-line-thickness, fill: design-colors-section-titles)
            ] else if design-section-titles-type == "with-full-line" [

              #v(design-text-font-size * 0.4)
              #box(width: 1fr, height: design-section-titles-line-thickness, fill: design-colors-section-titles)
            ]
          ]
        )
      ]
     ] + v(1em),
  )
  #v(-1em)
  // Vertical space after the section title
  #v(design-section-titles-vertical-space-below - 0.5em)
]

// Links:
#let original-link = link
#let link(url, body) = {
  body = [#if design-links-underline [#underline(body)] else [#body]]
  body = [#if design-links-use-external-link-icon [#body#h(design-text-font-size/4)#box(
        fa-icon("external-link", size: 0.7em),
        baseline: -10%,
      )] else [#body]]
  body = [#set text(fill: design-colors-links);#body]
  original-link(url, body)
}

// Last updated date text:
#if design-page-show-last-updated-date {
  let dx
  if design-section-titles-type == "moderncv" {
    dx = 0cm
  } else {
    dx = -design-entries-left-and-right-margin
  }
  place(
    top + right,
    dy: -design-page-top-margin / 2,
    dx: dx,
    text(
      [_#locale-catalog-last-updated-date-style _],
      fill: design-colors-last-updated-date-and-page-numbering,
      size: 0.9em,
    ),
  )
}

#let connections(connections-list) = context {
  set text(fill: design-colors-connections, font: design-header-connections-font-family)
  set par(leading: design-text-leading*1.7, justify: false)
  let list-of-connections = ()
  let separator = (
    h(design-header-horizontal-space-between-connections / 2, weak: true)
      + design-header-separator-between-connections
      + h(design-header-horizontal-space-between-connections / 2, weak: true)
  )
  let starting-index = 0
  while (starting-index < connections-list.len()) {
    let left-sum-right-margin
    if type(page.margin) == "dictionary" {
      left-sum-right-margin = page.margin.left + page.margin.right
    } else {
      left-sum-right-margin = page.margin * 4
    }

    let ending-index = starting-index + 1
    while (
      measure(connections-list.slice(starting-index, ending-index).join(separator)).width
        < page.width - left-sum-right-margin
    ) {
      ending-index = ending-index + 1
      if ending-index > connections-list.len() {
        break
      }
    }
    if ending-index > connections-list.len() {
      ending-index = connections-list.len()
    }
    list-of-connections.push(connections-list.slice(starting-index, ending-index).join(separator))
    starting-index = ending-index
  }
  align(list-of-connections.join(linebreak()), design-header-alignment)
  v(design-header-vertical-space-between-connections-and-first-section - design-section-titles-vertical-space-above)
}

#let three-col-entry(
  left-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  middle-content: "",
  right-content: "",
  alignments: (left, auto, right),
) = (
  if design-section-titles-type == "moderncv" [
    #three-col(
      left-column-width: right-column-width,
      middle-column-width: left-column-width,
      right-column-width: 1fr,
      left-content: right-content,
      middle-content: [
        #block(
          [
            #left-content
          ],
          inset: (
            left: design-entries-left-and-right-margin,
            right: design-entries-left-and-right-margin,
          ),
          breakable: design-entries-allow-page-break-in-entries,
          width: 100%,
        )
      ],
      right-content: middle-content,
      alignments: (design-text-date-and-location-column-alignment, left, auto),
    )
  ] else [
    #block(
      [
        #three-col(
          left-column-width: left-column-width,
          right-column-width: right-column-width,
          left-content: left-content,
          middle-content: middle-content,
          right-content: right-content,
          alignments: alignments,
        )
      ],
      inset: (
        left: design-entries-left-and-right-margin,
        right: design-entries-left-and-right-margin,
      ),
      breakable: design-entries-allow-page-break-in-entries,
      width: 100%,
    )
  ]
)

#let two-col-entry(
  left-column-width: 1fr,
  right-column-width: design-entries-date-and-location-width,
  left-content: "",
  right-content: "",
  alignments: (auto, design-text-date-and-location-column-alignment),
  column-gutter: design-entries-horizontal-space-between-columns,
) = (
  if design-section-titles-type == "moderncv" [
    #two-col(
      left-column-width: right-column-width,
      right-column-width: left-column-width,
      left-content: right-content,
      right-content: [
        #block(
          [
            #left-content
          ],
          inset: (
            left: design-entries-left-and-right-margin,
            right: design-entries-left-and-right-margin,
          ),
          breakable: design-entries-allow-page-break-in-entries,
          width: 100%,
        )
      ],
      alignments: (design-text-date-and-location-column-alignment, auto),
    )
  ] else [
    #block(
      [
        #two-col(
          left-column-width: left-column-width,
          right-column-width: right-column-width,
          left-content: left-content,
          right-content: right-content,
          alignments: alignments,
        )
      ],
      inset: (
        left: design-entries-left-and-right-margin,
        right: design-entries-left-and-right-margin,
      ),
      breakable: design-entries-allow-page-break-in-entries,
      width: 100%,
    )
  ]
)

#let one-col-entry(content: "") = [
  #let left-space = design-entries-left-and-right-margin
  #if design-section-titles-type == "moderncv" [
    #(left-space = left-space + design-entries-date-and-location-width + design-entries-horizontal-space-between-columns)
  ]
  #block(
    [#set par(spacing: design-text-leading); #content],
    breakable: design-entries-allow-page-break-in-entries,
    inset: (
      left: left-space,
      right: design-entries-left-and-right-margin,
    ),
    width: 100%,
  )
]

= 최재필

// Print connections:
#let connections-list = (
  [서울, 대한민국],
  [#box(original-link("mailto:chljeffreyz@gmail.com")[chljeffreyz\@gmail.com])],
  [#box(original-link("tel:+82-10-2589-5000")[010-2589-5000])],
)
#connections(connections-list)



== Education & Certificates


// YES DATE, NO DEGREE
#two-col-entry(
  left-content: [
    #strong[KAIST 경영대학], 석사, 금융공학
  ],
  right-content: [
    2024년 3월 – 현재
  ],
)
#block(
  [
    #set par(spacing: 0pt)
    
  ],
  inset: (
    left: design-entries-left-and-right-margin,
    right: design-entries-left-and-right-margin,
  ),
)

#v(design-entries-vertical-space-between-entries)
// YES DATE, NO DEGREE
#two-col-entry(
  left-content: [
    #strong[WorldQuant Online University], 석사, Financial Engineering
  ],
  right-content: [
    2023년 1월 – 현재
  ],
)
#block(
  [
    #set par(spacing: 0pt)
    
  ],
  inset: (
    left: design-entries-left-and-right-margin,
    right: design-entries-left-and-right-margin,
  ),
)

#v(design-entries-vertical-space-between-entries)
// YES DATE, NO DEGREE
#two-col-entry(
  left-content: [
    #strong[성균관대학교], 학사, Global Economics, \(부전공: Informatics\)
  ],
  right-content: [
    2013년 3월 – 2020년 8월
  ],
)
#block(
  [
    #set par(spacing: 0pt)
    
  ],
  inset: (
    left: design-entries-left-and-right-margin,
    right: design-entries-left-and-right-margin,
  ),
)

#v(design-entries-vertical-space-between-entries)
// NO DATE, NO DEGREE

#one-col-entry(
  content: [
    #strong[Certificates], 

    #v(-design-text-leading)
    #v(design-highlights-top-margin);#highlights([CFA: 1차 합격 \(2019\)],[KOFIA: 투자자산운용사 \(2019\), 파생상품투자권유자문인력 \(2023\), 펀드투자권유자문인력 \(2022\)],)
  ],
)



== Work Experience


#two-col-entry(
  left-content: [
    #strong[메리츠증권], 트레이딩본부 매크로트레이딩팀 \(파트타임, 학업 병행\)
  ],
  right-content: [
    2025년 1월 – 2025년 7월
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([내부 딜러들이 코딩 없이 글로벌 매크로\(채권\/주식인덱스\/원자재\/FX\) 전략을 엑셀 함수 입력하듯 만들 수 있는 플랫폼을 개발],[다양한 객체지향 디자인패턴을 도입하여 전략\/유틸 기능 추가가 용이하고 데이터 쿼리, 전\/후처리 등이 설정파일\(config\) 조작만으로 적용\/수정될 수 있도록 확장성을 고민해 설계],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[Zero One AI], 금융 리서치 하계 인턴
  ],
  right-content: [
    2024년 7월 – 2024년 8월
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([AQR 'Replication Crisis' 논문 기반 CRSP & Compustat \(WRDS\)를 활용한 퀀트 팩터 DB 구축 및 대량 API 문서 전처리를 통한 일별 팩터 데이터 생산용 확장 가능한 API 래퍼 개발],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[우리은행], 마이데이터 사업부 서비스 기획자
  ],
  right-content: [
    2022년 7월 – 2024년 2월
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([마이데이터 서비스 내 '내 투자 스토리' 개인화 데이터 큐레이션 기능 개발 주도. 스토리보드 작성, SQL\/Python 기반 EDA 수행 및 기능 출시 후 푸시 알림 응답률 11\% 달성\(1만 건 이상 발송 푸시 중 최고\)],[출시 후 A\/B 테스트를 통해 KPI 개선 효과 통계적 검증],[가입 관련 KPI 정의, SQL 활용 데이터 추출, 관리자 대시보드 설계를 통한 성과 모니터링 체계 구축],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[우리은행], 지점 근무
  ],
  right-content: [
    2021년 9월 – 2022년 3월
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([Excel 기반 기업대출 KPI 계산기를 개발하여, 지점장님의 기업 대출 실행 여부 의사결정 지원],[사내 제안광장에 30건 이상의 시스템·프로세스 개선안을 올려 우수 제안상 2위 수상 \(입사 후 3개월 이내\)],)
  ],
)

#v(design-entries-vertical-space-between-entries)
#two-col-entry(
  left-content: [
    #strong[HaaFor Research Korea], 퀀트 리서치 인턴
  ],
  right-content: [
    2020년 6월 – 2020년 11월
  ],
)
#one-col-entry(
  content: [
    #v(design-highlights-top-margin);#highlights([미국 주식 4,000+ 종목에 대한 대체 데이터 리서치 및 특허·뉴스·온라인 지표 활용 신규 데이터셋 구축해 다른 퀀트 리서쳐들의 상관관계 낮은 알파 전략 개발 지원],[일단위 리밸런싱 주기의 시장\/섹터\/팩터 중립적인 롱숏 알파 전략 개발 경험],)
  ],
)



== Projects



#one-col-entry(
  content: [
    #strong[kor-quant-dataloader] 

    #v(-design-text-leading)
    #v(design-highlights-top-margin);#highlights([생존 편향을 제거하고 데이터 로드 편의성을 높인 한국 주식 데이터셋 파이썬 패키지 개발 \(KRX 데이터\)],[날짜 범위만 지정하면 long format: 날짜-종목 인덱스, 각종 팩터 컬럼 형식 또는 wide format: 날짜 인덱스, 종목 컬럼 형식으로 데이터 반환],)
  ],
)

#v(design-entries-vertical-space-between-entries)

#one-col-entry(
  content: [
    #strong[qtrsch] 

    #v(-design-text-leading)
    #v(design-highlights-top-margin);#highlights([한국 주식 데이터로 파마-프렌치 5요인 모형 직접 구축 후 FnGuide 벤치마크와 팩터 수익률 검증],[팩터 기반 요소로 수익률 분해, Group Neutralization 효과 분석],[한국 시장에서 PEAD\(실적발표 후 주가이상현상\) 현상 심층 분석 및 실적 발표 전후 누적 수익률 시각화],)
  ],
)

#v(design-entries-vertical-space-between-entries)

#one-col-entry(
  content: [
    #strong[학술 논문 구현: 텍스트 마이닝을 활용한 금융통화위원회 의사록 분석 \(2019\)] 

    #v(-design-text-leading)
    #v(design-highlights-top-margin);#highlights([텍스트 마이닝 기법으로 금융통화위원회 의사록의 톤\(매파\/비둘기파\)을 측정하고 정책금리 변동과의 상관관계 분석],)
  ],
)



== Additional Information


#one-col-entry(
  content: [#strong[기술:] Python, Oracle SQL, Git-flow, 웹 스크래핑, MS-Office]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[언어:] 영어 \(TOEIC 985, TOEIC Speaking 180\), 독일어 \(Zertifikat Deutsch B1\)]
)
#v(design-entries-vertical-space-between-entries)
#one-col-entry(
  content: [#strong[병역:] 의무경찰 병장 만기전역 \(2014년 9월 - 2016년 6월\)]
)


