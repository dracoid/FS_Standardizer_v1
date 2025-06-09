# FS_standardizer_CF/general_mapper.py
"""
Industry-agnostic CF mapper – 3-digit sub-code 체계 (v3-fix)
‣ 남아있던 Unclassified 태그를 최대한 흡수 + 순환 import/문법 오류 제거
"""
from __future__ import annotations

from FS_standardizer_CF.utils.helper import clean_text


###############################################################################
# 1) Keyword buckets – **모두 소문자** substrings                            #
###############################################################################
# ───────── Operating
_OP_INT_PAID      = ("cashpaidforinterest", "interestpaid")
_OP_TAX_PAID      = ("cashpaidforincome", "incometaxespaid")
_OP_STOCK_COMP    = ("stockbasedcompensation", "sharebasedcompensation", "stockbasedcompensationnet")
_OP_DA            = (
    "depreciation", "amortization", "impairmentofproperty", "impairmentofintangible",
    "amortizationandimpairment", "depreciationandimpairment",
)
_OP_GAIN_LOSSSEC  = (
    "debtandequitysecuritiesgainloss", "gainlossonmarketable", "gainlossonnonmarketable",
    "gain on marketable", "gainondivestiture", "gainon equity interest",
)
_OP_WORKING_CAP   = (
    "increasedecreaseinaccounts", "increasedecreaseinaccrued",
    "increasedecreaseincontract", "increasedecreaseindeferredrevenue",
    "increasedecreaseinotheroperatingassets", "increasedecreaseinotheroperatingli",
    "increasedecreaseinincometaxes", "increasedecreaseinprepaid",
)
_OP_DEFERRED_TAX  = ("deferredincometax", "deferredincometaxesandtaxcredits")
_OP_NET_CASH      = (
    "netcashprovidedbyusedinoperatingactivities",
    "netcashprovidedbyusedinoperatingactivitiescontinuingoperations",
    "netcashprovidedbyusedinoperatingactivitiesdiscontinuedoperations",
    "cashgeneratedfromoperations",
)

# ───────── Investing
_INV_CAPEX        = (
    "capitalexpenditure", "capitalexpenditures",
    "paymentstoacquirepropertyplantandequipment",
)
_INV_PURCHASE     = (
    "purchaseofsecurities", "purchaseofmarketablesecurities",
    "purchasesofavailableforsale", "paymentstoacquiremarketablesecurities",
    "purchasesofnonmarketableinvestments", "purchasesofnonmarketablesecurities",
)
_INV_PROCEEDS     = (
    "proceedsfromsaleofassets", "proceedsfrommaturity",
    "proceedsfromsaleandmaturityofmarketablesecurities",
    "proceedsfromsaleofpropertyplantandequipment",
    "maturitiesandsalesofnonmarketable", "proceedsfromsaleandmaturityofotherinvestments",
    "divestiture", "stepacquisition",
)
_INV_OTHER        = (
    "otherinvestingactivities", "paymentsforproceedsfromotherinvestingactivities",
    "investmentsinreverserepurchaseagreements", "collateralheldundersecuritieslending",
)
_INV_BUSINESS_ACQ = (
    "paymentforbusinesscombination", "acquisitionofbusiness",
    "acquisitionsnetofcashacquired",
)
_INV_NOTES_COLL   = ("collectionofnotesreceivable",)
_INV_NET_CASH     = (
    "netcashprovidedbyusedininvestingactivities",
    "netcashprovidedbyusedininvestingactivitiescontinuingoperations",
)

# ───────── Financing
_FIN_DIVIDEND     = ("dividendspaid", "cashdividends", "paymentsofdividends", "adjustment payment")
_FIN_REPURCHASE   = ("repurchaseofcommonstock", "treasurystock", "stockbasedaward")
_FIN_DEBT_PROC    = ("proceedsfromissuanceofdebt", "proceedsfromdebt")
_FIN_DEBT_REPAY   = (
    "repaymentsofdebt", "repaymentsofdebtandcapitalleaseobligations",
    "repaymentsofdebtandcapitallease",
)
_FIN_MINORITY     = (
    "proceedsfromminorityshareholders", "proceedsfromsaleofinterestinconsolidatedentities",
    "proceedsfromsaleofsubsidiaryshares",
)
_FIN_PARENT_TX    = ("paymentsforparentcompanytransaction",)
_FIN_NET_CASH     = (
    "netcashprovidedbyusedinfinancingactivities",
    "netcashprovidedbyusedinfinancingactivitiescontinuingoperations",
)

# ───────── Supplemental / Summary
_SUPPL_EFFECT     = (
    "effectofexchangeratechangesoncash", "effectofexchangerateoncashandequivalents",
    "fxeffect", "exchangerate",
)
_SUPPL_NONCASH    = (
    "noncashinvestingandfinancingactivities",
    "supplementalscheduleofnoncashinvestingandfinancingactivities",
)
_SUPPL_CASH_BEGIN = ("cashandcashequivalentsatbeginning",)
_SUPPL_CASH_END   = ("cashandcashequivalentsatend",)
_SUPPL_CASH_NET   = (
    "cashequivalentsperiodincrease", "netincrease(decrease)incash",
    "netdecreaseincash",
)

###############################################################################
# 2) Helper
###############################################################################
def _build(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"


###############################################################################
# 3) Public mapper
###############################################################################
def classify_general_cf(tag: str, segments: str | None, plabel: str | None):  # noqa: C901
    """Fallback CF mapper – returns (category, subcategory, id, id_label)"""
    t = tag.lower()

    # ── Operating
    if any(k in t for k in _OP_INT_PAID):      return _build("01. Operating Activities", "191. Interest Paid", segments, plabel, tag)
    if any(k in t for k in _OP_TAX_PAID):      return _build("01. Operating Activities", "193. Income Taxes Paid", segments, plabel, tag)
    if any(k in t for k in _OP_STOCK_COMP):    return _build("01. Operating Activities", "150. Stock-based Compensation", segments, plabel, tag)
    if any(k in t for k in _OP_DA):            return _build("01. Operating Activities", "155. Depreciation & Amortization", segments, plabel, tag)
    if any(k in t for k in _OP_GAIN_LOSSSEC):  return _build("01. Operating Activities", "170. Gain/Loss on Securities", segments, plabel, tag)
    if any(k in t for k in _OP_WORKING_CAP):   return _build("01. Operating Activities", "180. Working-capital Changes", segments, plabel, tag)
    if any(k in t for k in _OP_DEFERRED_TAX):  return _build("01. Operating Activities", "160. Deferred Tax Adjustment", segments, plabel, tag)
    if any(k in t for k in _OP_NET_CASH):      return _build("01. Operating Activities", "199. Net Cash from Operating", segments, plabel, tag)

    # ── Investing
    if any(k in t for k in _INV_CAPEX):        return _build("02. Investing Activities", "210. Capital Expenditures", segments, plabel, tag)
    if any(k in t for k in _INV_BUSINESS_ACQ): return _build("02. Investing Activities", "230. Business Combinations & Intangible", segments, plabel, tag)
    if any(k in t for k in _INV_PURCHASE):     return _build("02. Investing Activities", "240. Securities Purchased", segments, plabel, tag)
    if any(k in t for k in _INV_PROCEEDS):     return _build("02. Investing Activities", "241. Securities / Asset Proceeds", segments, plabel, tag)
    if any(k in t for k in _INV_NOTES_COLL):   return _build("02. Investing Activities", "250. Collection of Notes", segments, plabel, tag)
    if any(k in t for k in _INV_OTHER):        return _build("02. Investing Activities", "260. Other Investing", segments, plabel, tag)
    if any(k in t for k in _INV_NET_CASH):     return _build("02. Investing Activities", "299. Net Cash from Investing", segments, plabel, tag)

    # ── Financing
    if any(k in t for k in _FIN_DIVIDEND):     return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)
    if any(k in t for k in _FIN_REPURCHASE):   return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DEBT_PROC):    return _build("03. Financing Activities", "340. Proceeds from Debt", segments, plabel, tag)
    if any(k in t for k in _FIN_DEBT_REPAY):   return _build("03. Financing Activities", "341. Repayments of Debt", segments, plabel, tag)
    if any(k in t for k in _FIN_MINORITY):     return _build("03. Financing Activities", "350. Minority-interest Proceeds", segments, plabel, tag)
    if any(k in t for k in _FIN_PARENT_TX):    return _build("03. Financing Activities", "360. Parent-company Transactions", segments, plabel, tag)
    if any(k in t for k in _FIN_NET_CASH):     return _build("03. Financing Activities", "399. Net Cash from Financing", segments, plabel, tag)

    # ── Supplemental / Reconciliation
    if any(k in t for k in _SUPPL_CASH_BEGIN): return _build("04. Supplemental", "430. Cash & CE – Beginning", segments, plabel, tag)
    if any(k in t for k in _SUPPL_CASH_END):   return _build("04. Supplemental", "431. Cash & CE – End", segments, plabel, tag)
    if any(k in t for k in _SUPPL_CASH_NET):   return _build("04. Supplemental", "440. Net Change in Cash", segments, plabel, tag)
    if any(k in t for k in _SUPPL_EFFECT):     return _build("04. Supplemental", "410. FX Effect on Cash", segments, plabel, tag)
    if any(k in t for k in _SUPPL_NONCASH):    return _build("04. Supplemental", "420. Non-cash Invest & Finance", segments, plabel, tag)

    # ── Unclassified
    return None, None, None, None


# fallback alias – bank/energy/insurance mapper에서 import
classify_general = classify_general_cf