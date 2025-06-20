# SEC XBRL

## Installation (TODO)

## Example (TODO)

## How it works (working on this).

eXtensible Business Reporting Language (XBRL) is embedded in certain SEC documents, such as 10-Ks, in the form of inline XBRL.

### Data Files

XBRL files submitted to the sec consist of the inline xbrl, definition, schema, label, calculation, and presentation documents.

#### Example (Tesla 10-K)

| #   | Description                                              | File                      | Type        | Size     |
|-----|----------------------------------------------------------|---------------------------|------------|---------|
| 1   | 10-K                                                     | tsla-20221231.htm         | iXBRL      | 7964288 |
| ... | ...                                                      | ...                       | ...        | ...     |
| 9   | XBRL TAXONOMY EXTENSION DEFINITION LINKBASE DOCUMENT     | tsla-20221231_def.xml     | EX-101.DEF | 550438  |
| 10  | XBRL TAXONOMY EXTENSION SCHEMA DOCUMENT                  | tsla-20221231.xsd         | EX-101.SCH | 147812  |
| 11  | XBRL TAXONOMY EXTENSION LABEL LINKBASE DOCUMENT          | tsla-20221231_lab.xml     | EX-101.LAB | 1070835 |
| 12  | XBRL TAXONOMY EXTENSION CALCULATION LINKBASE DOCUMENT    | tsla-20221231_cal.xml     | EX-101.CAL | 136183  |
| 13  | XBRL TAXONOMY EXTENSION PRESENTATION LINKBASE DOCUMENT   | tsla-20221231_pre.xml     | EX-101.PRE | 843204  |

#### Inline XBRL

Much of the inline xbrl is in the top of the document.

```<body style="margin: auto!important;padding: 8px;">
    <div style="display:none;">
        <ix:header>
            <ix:hidden> ...
            </ix:hidden>
            <ix:references>
            </ix:references>
            <ix:resources> ...
            </ix:resources>
        </ix:header>
    </div>
    ....
</body>
```

The ix:hidden tag looks like this:
```
...
<ix:nonNumeric id="F_ded02aad-d116-4cb6-9088-0a119c5d030a" name="dei:AmendmentFlag" contextRef="C_b6c8c636-658e-4c1f-97de-bb0bd181ac0d">false</ix:nonNumeric>
...
```

ix:reference provides the link to the schema document.
```
<ix:references>
    <link:schemaRef xlink:type="simple" xlink:href="tsla-20221231.xsd"></link:schemaRef>
</ix:references>
```

ix:resources
```
...
<xbrli:context id="C_e95148b7-bbbd-4e37-bd18-06e7efa3e132">
    <xbrli:entity>
        <xbrli:identifier scheme="http://www.sec.gov/CIK">0001318605</xbrli:identifier>
        <xbrli:segment>
            <xbrldi:explicitMember dimension="us-gaap:LongtermDebtTypeAxis">tsla:NonrecourseDebtMember
            </xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="us-gaap:DebtInstrumentAxis">tsla:CashEquityDebtMember
            </xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="srt:RangeAxis">srt:MinimumMember</xbrldi:explicitMember>
        </xbrli:segment>
    </xbrli:entity>
    <xbrli:period>
        <xbrli:instant>2021-12-31</xbrli:instant>
    </xbrli:period>
</xbrli:context>
...
```