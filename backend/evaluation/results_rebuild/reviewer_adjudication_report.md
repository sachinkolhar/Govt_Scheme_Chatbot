# Reviewer Adjudication Report

> **Warning:** `original_expected_scheme` is an unverified source label, not ground truth. Candidate rank, string similarity, traceability, FAISS distance, and dataset row counts must not be treated as semantic correctness. FAISS index-to-dataset row alignment is not verified.

This report is generated from the pending rows in `backend/evaluation/label_audit_reports/manual_review_worksheet.csv`, the current `dataset/govt_schemes.csv`, and the blank `label_decisions.csv` template. It contains no prefilled decisions or reviewer conclusions.

- Pending queries: 40
- Candidate entries: 120
- Dataset fields inspected: scheme_name, slug, details, benefits, eligibility, application, documents, level, schemeCategory, Unnamed: 9, tags
- Missing versus empty fields: `[FIELD NOT PRESENT IN DATASET]` means the column does not exist; `[FIELD PRESENT BUT EMPTY]` means the column exists but the selected cell is blank.

## Review Prompts

After each candidate, complete the prompts without inferring from the source label or ranking:

```text
decision:
verified_dataset_slug:
rationale:
evidence_reference:
reviewer_id:
confidence:
second_review_status:
notes:
```

## Query 7

- **Query text:** senior citizen pension scheme
- **Original source label (unverified):** Indira Gandhi National Old Age Pension Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1433
- **Candidate slug:** `igoapsm`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme (Maharashtra)
- **Details:** The scheme "Indira Gandhi National Old Age Pension" is a social welfare scheme by the Social Justice &amp; Special Assistance Department, Government of Maharashtra. In this scheme, ₹600 per month is provided to elderly individuals aged 65 years and above from BPL families.
- **Eligibility:** The applicant should be a resident of Maharashtra. The applicant should be 65 years of age or older. The applicant should be from a Below Poverty Line (BPL) family. The applicant should not be receiving pension benefits under any social security scheme.
- **Benefits/scope:** A monthly financial assistance of ₹600/-.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1434
- **Candidate slug:** `ignoapsp`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme (Punjab)
- **Details:** The "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)" is a social welfare initiative by the Department of Social Security and Development of Women and Children, Government of Punjab. In this scheme, persons aged between 60 and 79 years receive a pension of ₹200/- per month, while those aged 80 years and above receive ₹500/- per month. The scheme applies only to persons belonging to the Below Poverty Line (BPL) category.
- **Eligibility:** The applicant should be a resident of Punjab. The applicant should be 60 years of age or older. The applicant should be from a Below Poverty Line (BPL) family. The applicant should not be receiving pension benefits under any social security scheme.
- **Benefits/scope:** ₹200/- month, for persons aged 60 to 79 years. ₹500/- month, for persons aged 80 years and above.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1435
- **Candidate slug:** `ignoaps-sikkim`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme - Sikkim
- **Details:** The scheme “Indira Gandhi National Old Age Pension Scheme (IGNOAPS)” was started by the Department of Women &amp; Child Welfare, Govt. of Sikkim in 2014. Under this scheme, a pension is provided to elderly citizens above the age of 60 years belonging to the Below Poverty Line (BPL) category and the beneficiary will receive a monthly pension of ₹ 1500/-, ₹ 2000/- &amp; ₹ 2500/- as per eligibility criteria.
- **Eligibility:** The applicant should be a resident of the state of Sikkim. The applicant should be from Below Poverty Line (BPL) family. The applicant should have attained the age of 60 years and above. The applicant should not have any source of income. The applicant should not be a recipient of salary/pension/family pension from Central Government / other State Governments. The applicant should have opened the Bank Account under “Pradhan Mantri Jan Dhan Yojana”. ﻿ Note 01: In case both the husband &amp; wife are old age persons and are eligible for Indira Gandhi National Old Age Pension Scheme (IGNOAPS), only one member of the family shall be awarded the pension. In case of death of the pensioner, such pension shall be transferred to his/her spouse, if alive on surrender of the passbook, provided he/she has attained the age of 60 (sixty) years of age or more. ﻿ Note 02: Each beneficiary of the Pensions should submit "Life Certificate" in the prescribed format in the month of November every year failing which it will be presumed that the beneficiary is either died or migrated outside the State of Sikkim and the payment of pension shall be stopped forthwith without further notice. ﻿
- **Benefits/scope:** A monthly pension of ₹ 1500/- to the old aged person between the age group of 60 years – 69 years. A monthly pension of ₹ 2000/- to the old aged person between the age group of 70 years + and above. A monthly pension of ₹ 2500/- to the old aged persons having attained the age of 80 years and above. The beneficiary will get a pension as long as he/she is alive.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 8

- **Query text:** old age pension benefits
- **Original source label (unverified):** Indira Gandhi National Old Age Pension Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1433
- **Candidate slug:** `igoapsm`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme (Maharashtra)
- **Details:** The scheme "Indira Gandhi National Old Age Pension" is a social welfare scheme by the Social Justice &amp; Special Assistance Department, Government of Maharashtra. In this scheme, ₹600 per month is provided to elderly individuals aged 65 years and above from BPL families.
- **Eligibility:** The applicant should be a resident of Maharashtra. The applicant should be 65 years of age or older. The applicant should be from a Below Poverty Line (BPL) family. The applicant should not be receiving pension benefits under any social security scheme.
- **Benefits/scope:** A monthly financial assistance of ₹600/-.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1434
- **Candidate slug:** `ignoapsp`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme (Punjab)
- **Details:** The "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)" is a social welfare initiative by the Department of Social Security and Development of Women and Children, Government of Punjab. In this scheme, persons aged between 60 and 79 years receive a pension of ₹200/- per month, while those aged 80 years and above receive ₹500/- per month. The scheme applies only to persons belonging to the Below Poverty Line (BPL) category.
- **Eligibility:** The applicant should be a resident of Punjab. The applicant should be 60 years of age or older. The applicant should be from a Below Poverty Line (BPL) family. The applicant should not be receiving pension benefits under any social security scheme.
- **Benefits/scope:** ₹200/- month, for persons aged 60 to 79 years. ₹500/- month, for persons aged 80 years and above.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1435
- **Candidate slug:** `ignoaps-sikkim`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme - Sikkim
- **Details:** The scheme “Indira Gandhi National Old Age Pension Scheme (IGNOAPS)” was started by the Department of Women &amp; Child Welfare, Govt. of Sikkim in 2014. Under this scheme, a pension is provided to elderly citizens above the age of 60 years belonging to the Below Poverty Line (BPL) category and the beneficiary will receive a monthly pension of ₹ 1500/-, ₹ 2000/- &amp; ₹ 2500/- as per eligibility criteria.
- **Eligibility:** The applicant should be a resident of the state of Sikkim. The applicant should be from Below Poverty Line (BPL) family. The applicant should have attained the age of 60 years and above. The applicant should not have any source of income. The applicant should not be a recipient of salary/pension/family pension from Central Government / other State Governments. The applicant should have opened the Bank Account under “Pradhan Mantri Jan Dhan Yojana”. ﻿ Note 01: In case both the husband &amp; wife are old age persons and are eligible for Indira Gandhi National Old Age Pension Scheme (IGNOAPS), only one member of the family shall be awarded the pension. In case of death of the pensioner, such pension shall be transferred to his/her spouse, if alive on surrender of the passbook, provided he/she has attained the age of 60 (sixty) years of age or more. ﻿ Note 02: Each beneficiary of the Pensions should submit "Life Certificate" in the prescribed format in the month of November every year failing which it will be presumed that the beneficiary is either died or migrated outside the State of Sikkim and the payment of pension shall be stopped forthwith without further notice. ﻿
- **Benefits/scope:** A monthly pension of ₹ 1500/- to the old aged person between the age group of 60 years – 69 years. A monthly pension of ₹ 2000/- to the old aged person between the age group of 70 years + and above. A monthly pension of ₹ 2500/- to the old aged persons having attained the age of 80 years and above. The beneficiary will get a pension as long as he/she is alive.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 9

- **Query text:** pension for elderly citizens
- **Original source label (unverified):** Indira Gandhi National Old Age Pension Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1433
- **Candidate slug:** `igoapsm`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme (Maharashtra)
- **Details:** The scheme "Indira Gandhi National Old Age Pension" is a social welfare scheme by the Social Justice &amp; Special Assistance Department, Government of Maharashtra. In this scheme, ₹600 per month is provided to elderly individuals aged 65 years and above from BPL families.
- **Eligibility:** The applicant should be a resident of Maharashtra. The applicant should be 65 years of age or older. The applicant should be from a Below Poverty Line (BPL) family. The applicant should not be receiving pension benefits under any social security scheme.
- **Benefits/scope:** A monthly financial assistance of ₹600/-.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1434
- **Candidate slug:** `ignoapsp`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme (Punjab)
- **Details:** The "Indira Gandhi National Old Age Pension Scheme (IGNOAPS)" is a social welfare initiative by the Department of Social Security and Development of Women and Children, Government of Punjab. In this scheme, persons aged between 60 and 79 years receive a pension of ₹200/- per month, while those aged 80 years and above receive ₹500/- per month. The scheme applies only to persons belonging to the Below Poverty Line (BPL) category.
- **Eligibility:** The applicant should be a resident of Punjab. The applicant should be 60 years of age or older. The applicant should be from a Below Poverty Line (BPL) family. The applicant should not be receiving pension benefits under any social security scheme.
- **Benefits/scope:** ₹200/- month, for persons aged 60 to 79 years. ₹500/- month, for persons aged 80 years and above.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1435
- **Candidate slug:** `ignoaps-sikkim`
- **Scheme name/title:** Indira Gandhi National Old Age Pension Scheme - Sikkim
- **Details:** The scheme “Indira Gandhi National Old Age Pension Scheme (IGNOAPS)” was started by the Department of Women &amp; Child Welfare, Govt. of Sikkim in 2014. Under this scheme, a pension is provided to elderly citizens above the age of 60 years belonging to the Below Poverty Line (BPL) category and the beneficiary will receive a monthly pension of ₹ 1500/-, ₹ 2000/- &amp; ₹ 2500/- as per eligibility criteria.
- **Eligibility:** The applicant should be a resident of the state of Sikkim. The applicant should be from Below Poverty Line (BPL) family. The applicant should have attained the age of 60 years and above. The applicant should not have any source of income. The applicant should not be a recipient of salary/pension/family pension from Central Government / other State Governments. The applicant should have opened the Bank Account under “Pradhan Mantri Jan Dhan Yojana”. ﻿ Note 01: In case both the husband &amp; wife are old age persons and are eligible for Indira Gandhi National Old Age Pension Scheme (IGNOAPS), only one member of the family shall be awarded the pension. In case of death of the pensioner, such pension shall be transferred to his/her spouse, if alive on surrender of the passbook, provided he/she has attained the age of 60 (sixty) years of age or more. ﻿ Note 02: Each beneficiary of the Pensions should submit "Life Certificate" in the prescribed format in the month of November every year failing which it will be presumed that the beneficiary is either died or migrated outside the State of Sikkim and the payment of pension shall be stopped forthwith without further notice. ﻿
- **Benefits/scope:** A monthly pension of ₹ 1500/- to the old aged person between the age group of 60 years – 69 years. A monthly pension of ₹ 2000/- to the old aged person between the age group of 70 years + and above. A monthly pension of ₹ 2500/- to the old aged persons having attained the age of 80 years and above. The beneficiary will get a pension as long as he/she is alive.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 10

- **Query text:** health insurance for poor
- **Original source label (unverified):** Pradhan Mantri Jan Arogya Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2421
- **Candidate slug:** `pmjdy`
- **Scheme name/title:** Pradhan Mantri Jan Dhan Yojana
- **Details:** A  National Mission for Financial Inclusion (NMFI), namely, Pradhan Mantri Jan Dhan Yojana (PMJDY) was launched across the Country  in August, 2014 by the Prime Minister with the idea to ensure that citizens envisage their financial activities. PMJDY provides universal banking services for every unbanked household, based on the guiding principles of banking the unbanked, securing the unsecured, funding the unfunded and serving unserved and underserved areas. In order to give impetus to financial inclusion initiatives of the Government, PMJDY scheme was extended beyond 14.08.2018 with the focus on opening of accounts shifting from “every household” to “every unbanked adult”. The scheme has been made more attractive with upward revision in (i)	  OD limit from Rs. 5,000/- to Rs. 10,000/- and (ii)  Accidental  insurance cover on RuPay card holders from Rs.1 lakh to Rs.2 lakhs. PMJDY has been successful in increasing banking penetration and promoting financial inclusion across the country. The scheme has ensured access to various financial services like availability of basic savings bank account, access to need based credit, remittances facility, insurance and pension to the excluded sections i.e. weaker sections &amp; low-income groups.
- **Eligibility:** The applicant should be an Indian National. If minors above ten years apply, they will require support from their legal guardians for administering their PMJDY account.
- **Benefits/scope:** Basic Savings Bank Deposit Account (BSBDA) Any Indian citizen eligible to open a regular bank account can open a BSBDA. Such an account does not require any minimum balance maintenance. The account holders can use both bank branches, ATMs and Banking Correspondents (BCs) for depositing and withdrawing cash. However, one cannot withdraw cash more than four times a month. Small Account/Chota Khata Under Jan Dhan Yojana, people can open small bank accounts without presenting legal documents. These accounts would be valid normally for a period of twelve months. Thereafter, such accounts  would be allowed to a continue for a further period of twelve more months, if the account-holder provides a document showing that he/she has applied for any of the Officially Valid Document, within 12 months of opening the small account. RuPay Debit Card with inbuilt accident insurance Under PMJDY,  a free Rupay debit card,  with inbuilt accident insurance cover of Rs.2 lakhs (Rs 1 lakh for accounts opened before 28.08.2018),  is issued to all beneficiaries. Overdraft Facility Under PMJDY, beneficiaries can avail OD facility upto Rs. 10,000/-. Business Correspondents (BCs)/Bank Mitras  BCs/Bank Mitras are retail agents engaged by banks for providing banking services at locations other than a bank branch/ATM. It is mainly meant  for the rural areas, where bank branches are far-flung. BCs/Bank Mitras connect with the residents and guide them with banking solutions such as savings accounts, deposits, payments and withdrawals, mini account statements, etc. Banks with their strong network of BCs/Bank Mitras are providing hassle free services to the customers in remote / rural areas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2410
- **Candidate slug:** `pmagy`
- **Scheme name/title:** Pradhan Mantri Adarsh Gram Yojana
- **Details:** With a view to enabling an area-based development approach, a new scheme Pradhan Mantri Adarsh Gram Yojana (PMAGY) was launched during 2009-10. The Scheme aims at integrated development of Scheduled Castes majority villages. ﻿ The principal objective of PMAGY is the integrated development of SC majority Villages: (a) Primarily through convergent implementation of the relevant Central and State/UT Government Schemes; and (b) By taking up identified activities, which do not get covered under the existing Central and State Government Schemes, through ‘Gap-filling’ funds provided as Central Assistance to the extent of ₹20,00,000 per village. ﻿ The implementation of the Scheme was started on Pilot basis in 2009-10 and a total of 1000 villages was selected from 05 States namely Tamil Nadu (225), Rajasthan (225), Bihar (225), Himachal Pradesh (225) and Assam (100) were selected for this phase. All these 1000 villages have so far been declared as ‘Adarsh Gram’ by the respective State Governments. ﻿ The vision of an ‘Adarsh Gram' An ‘Adarsh Gram’ is one wherein people have access to various basic services so that the minimum needs of all the sections of society are fully met and disparities are reduced to a minimum. These villages would have all such infrastructure and their residents will have access to all such basic services that are necessary for a dignified living, creating thereby an environment in which everyone is enabled to utilize her/his potential to the fullest. ﻿
- **Eligibility:** Out of the villages having more than 50% SC population, only those with a total population greater than 500 will be eligible for selection in descending order of their SC population in the first instance under the Scheme. (As per the Census 2011, there are 46844 villages having more than 50% Scheduled Castes population. These villages are spread over 570 districts of 25 States &amp; UTs.) ﻿
- **Benefits/scope:** Physical Infrastructure 1.  Should be connected to the nearest major road by an all-weather road. Likewise, in the case of a multi-hamlet village, all hamlets should be connected with each other by an all-weather road. 2.  Access for all to safe drinking water on a sustainable basis. 3.  All houses should have electricity. 4.  The village should have slush-free internal roads and adequate street lighting. 5.  The village should have adequate communication facilities, such as post-office, telephones, and, if possible, internet, and Bharat Nirman Common Service Centre (being established by the Deptt. of Information Technology). 6.  Availability of adequate banking facilities through regular (brick and mortar) branches in the village or in close proximity, and through the Business Correspondent/Business Facilitator Model. 7.  All residents should have adequate housing, and there should be no homeless families. ﻿ Sanitation and Environment 1.  The village should have a high degree of sanitation- it should be free from dry latrines, and open defecation, and should have sanitary toilets, drains, and an efficient waste disposal system. It should, as far as possible, fulfill “Nirmal Gram Puraskar” norms. 2.  The Village should take care of its environment through (1) planting trees, (2) water harvest action and maintenance of water bodies (3) use of renewable sources of energy, such as biogas, solar energy, wind energy, use of smokeless chulhas, etc. ﻿ Social Infrastructure, Human Development, and Social Harmony 1.  Should have an Anganwadi center and schools of appropriate levels. 2.  The village should have adequate and attractive buildings for its Anganwadi, school, health center, panchayat, and community hall. The village should have adequate facilities for sports and other physical activities. 3.  All children in the age group of 3-6 should be enrolled in, and regularly attend the Anganwadi. Likewise, all children in the 6-14 age group should be enrolled in, and regularly attend school. 4.  All adults should be at least functionally literate and should have access to facilities for continuing education. 5.  Access for all to primary health care and Reproductive Child Health (RCH) facilities, with proper pre-natal and ante-natal care for mothers. 6.  100% institutional deliveries, full immunization of children, and observance of the small family norm. 7.  The village as a community should take special care of its women, children (especially girls), senior citizens, and persons with disabilities. 8.  There should be no public consumption of liquor or any other intoxicating substances, and their use, in general, should be discouraged. 9.  The village should have an active Gram Sabha/Gram Panchayat, women’s/swarozgaris’ Self-help Group, youth club, and Mahila Mandal. 10.  There should be no caste-based discrimination, complete eradication of untouchability, and a due sense of security and dignity among the weaker sections. 11.  Residents of the village should be aware of and exercise their constitutional and legal rights. Likewise, they should also be aware of and discharge their fundamental and civic duties. ﻿ Livelihood 1.  All youth and adults of the village should have adequate employment and means of livelihood, and there should be adequate arrangements for the development of skills among them so that as many of them as possible are in skilled employment. 2.  Progressive and efficient practices, based on new technology, should be used in all the economic activities pursued in the village, especially in agriculture, animal husbandry, fisheries, etc. 3.  Should have adequate access to remunerative prices for agricultural and other products of the village. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 11

- **Query text:** ayushman bharat scheme
- **Original source label (unverified):** Pradhan Mantri Jan Arogya Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2421
- **Candidate slug:** `pmjdy`
- **Scheme name/title:** Pradhan Mantri Jan Dhan Yojana
- **Details:** A  National Mission for Financial Inclusion (NMFI), namely, Pradhan Mantri Jan Dhan Yojana (PMJDY) was launched across the Country  in August, 2014 by the Prime Minister with the idea to ensure that citizens envisage their financial activities. PMJDY provides universal banking services for every unbanked household, based on the guiding principles of banking the unbanked, securing the unsecured, funding the unfunded and serving unserved and underserved areas. In order to give impetus to financial inclusion initiatives of the Government, PMJDY scheme was extended beyond 14.08.2018 with the focus on opening of accounts shifting from “every household” to “every unbanked adult”. The scheme has been made more attractive with upward revision in (i)	  OD limit from Rs. 5,000/- to Rs. 10,000/- and (ii)  Accidental  insurance cover on RuPay card holders from Rs.1 lakh to Rs.2 lakhs. PMJDY has been successful in increasing banking penetration and promoting financial inclusion across the country. The scheme has ensured access to various financial services like availability of basic savings bank account, access to need based credit, remittances facility, insurance and pension to the excluded sections i.e. weaker sections &amp; low-income groups.
- **Eligibility:** The applicant should be an Indian National. If minors above ten years apply, they will require support from their legal guardians for administering their PMJDY account.
- **Benefits/scope:** Basic Savings Bank Deposit Account (BSBDA) Any Indian citizen eligible to open a regular bank account can open a BSBDA. Such an account does not require any minimum balance maintenance. The account holders can use both bank branches, ATMs and Banking Correspondents (BCs) for depositing and withdrawing cash. However, one cannot withdraw cash more than four times a month. Small Account/Chota Khata Under Jan Dhan Yojana, people can open small bank accounts without presenting legal documents. These accounts would be valid normally for a period of twelve months. Thereafter, such accounts  would be allowed to a continue for a further period of twelve more months, if the account-holder provides a document showing that he/she has applied for any of the Officially Valid Document, within 12 months of opening the small account. RuPay Debit Card with inbuilt accident insurance Under PMJDY,  a free Rupay debit card,  with inbuilt accident insurance cover of Rs.2 lakhs (Rs 1 lakh for accounts opened before 28.08.2018),  is issued to all beneficiaries. Overdraft Facility Under PMJDY, beneficiaries can avail OD facility upto Rs. 10,000/-. Business Correspondents (BCs)/Bank Mitras  BCs/Bank Mitras are retail agents engaged by banks for providing banking services at locations other than a bank branch/ATM. It is mainly meant  for the rural areas, where bank branches are far-flung. BCs/Bank Mitras connect with the residents and guide them with banking solutions such as savings accounts, deposits, payments and withdrawals, mini account statements, etc. Banks with their strong network of BCs/Bank Mitras are providing hassle free services to the customers in remote / rural areas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2410
- **Candidate slug:** `pmagy`
- **Scheme name/title:** Pradhan Mantri Adarsh Gram Yojana
- **Details:** With a view to enabling an area-based development approach, a new scheme Pradhan Mantri Adarsh Gram Yojana (PMAGY) was launched during 2009-10. The Scheme aims at integrated development of Scheduled Castes majority villages. ﻿ The principal objective of PMAGY is the integrated development of SC majority Villages: (a) Primarily through convergent implementation of the relevant Central and State/UT Government Schemes; and (b) By taking up identified activities, which do not get covered under the existing Central and State Government Schemes, through ‘Gap-filling’ funds provided as Central Assistance to the extent of ₹20,00,000 per village. ﻿ The implementation of the Scheme was started on Pilot basis in 2009-10 and a total of 1000 villages was selected from 05 States namely Tamil Nadu (225), Rajasthan (225), Bihar (225), Himachal Pradesh (225) and Assam (100) were selected for this phase. All these 1000 villages have so far been declared as ‘Adarsh Gram’ by the respective State Governments. ﻿ The vision of an ‘Adarsh Gram' An ‘Adarsh Gram’ is one wherein people have access to various basic services so that the minimum needs of all the sections of society are fully met and disparities are reduced to a minimum. These villages would have all such infrastructure and their residents will have access to all such basic services that are necessary for a dignified living, creating thereby an environment in which everyone is enabled to utilize her/his potential to the fullest. ﻿
- **Eligibility:** Out of the villages having more than 50% SC population, only those with a total population greater than 500 will be eligible for selection in descending order of their SC population in the first instance under the Scheme. (As per the Census 2011, there are 46844 villages having more than 50% Scheduled Castes population. These villages are spread over 570 districts of 25 States &amp; UTs.) ﻿
- **Benefits/scope:** Physical Infrastructure 1.  Should be connected to the nearest major road by an all-weather road. Likewise, in the case of a multi-hamlet village, all hamlets should be connected with each other by an all-weather road. 2.  Access for all to safe drinking water on a sustainable basis. 3.  All houses should have electricity. 4.  The village should have slush-free internal roads and adequate street lighting. 5.  The village should have adequate communication facilities, such as post-office, telephones, and, if possible, internet, and Bharat Nirman Common Service Centre (being established by the Deptt. of Information Technology). 6.  Availability of adequate banking facilities through regular (brick and mortar) branches in the village or in close proximity, and through the Business Correspondent/Business Facilitator Model. 7.  All residents should have adequate housing, and there should be no homeless families. ﻿ Sanitation and Environment 1.  The village should have a high degree of sanitation- it should be free from dry latrines, and open defecation, and should have sanitary toilets, drains, and an efficient waste disposal system. It should, as far as possible, fulfill “Nirmal Gram Puraskar” norms. 2.  The Village should take care of its environment through (1) planting trees, (2) water harvest action and maintenance of water bodies (3) use of renewable sources of energy, such as biogas, solar energy, wind energy, use of smokeless chulhas, etc. ﻿ Social Infrastructure, Human Development, and Social Harmony 1.  Should have an Anganwadi center and schools of appropriate levels. 2.  The village should have adequate and attractive buildings for its Anganwadi, school, health center, panchayat, and community hall. The village should have adequate facilities for sports and other physical activities. 3.  All children in the age group of 3-6 should be enrolled in, and regularly attend the Anganwadi. Likewise, all children in the 6-14 age group should be enrolled in, and regularly attend school. 4.  All adults should be at least functionally literate and should have access to facilities for continuing education. 5.  Access for all to primary health care and Reproductive Child Health (RCH) facilities, with proper pre-natal and ante-natal care for mothers. 6.  100% institutional deliveries, full immunization of children, and observance of the small family norm. 7.  The village as a community should take special care of its women, children (especially girls), senior citizens, and persons with disabilities. 8.  There should be no public consumption of liquor or any other intoxicating substances, and their use, in general, should be discouraged. 9.  The village should have an active Gram Sabha/Gram Panchayat, women’s/swarozgaris’ Self-help Group, youth club, and Mahila Mandal. 10.  There should be no caste-based discrimination, complete eradication of untouchability, and a due sense of security and dignity among the weaker sections. 11.  Residents of the village should be aware of and exercise their constitutional and legal rights. Likewise, they should also be aware of and discharge their fundamental and civic duties. ﻿ Livelihood 1.  All youth and adults of the village should have adequate employment and means of livelihood, and there should be adequate arrangements for the development of skills among them so that as many of them as possible are in skilled employment. 2.  Progressive and efficient practices, based on new technology, should be used in all the economic activities pursued in the village, especially in agriculture, animal husbandry, fisheries, etc. 3.  Should have adequate access to remunerative prices for agricultural and other products of the village. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 12

- **Query text:** medical coverage government
- **Original source label (unverified):** Pradhan Mantri Jan Arogya Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2421
- **Candidate slug:** `pmjdy`
- **Scheme name/title:** Pradhan Mantri Jan Dhan Yojana
- **Details:** A  National Mission for Financial Inclusion (NMFI), namely, Pradhan Mantri Jan Dhan Yojana (PMJDY) was launched across the Country  in August, 2014 by the Prime Minister with the idea to ensure that citizens envisage their financial activities. PMJDY provides universal banking services for every unbanked household, based on the guiding principles of banking the unbanked, securing the unsecured, funding the unfunded and serving unserved and underserved areas. In order to give impetus to financial inclusion initiatives of the Government, PMJDY scheme was extended beyond 14.08.2018 with the focus on opening of accounts shifting from “every household” to “every unbanked adult”. The scheme has been made more attractive with upward revision in (i)	  OD limit from Rs. 5,000/- to Rs. 10,000/- and (ii)  Accidental  insurance cover on RuPay card holders from Rs.1 lakh to Rs.2 lakhs. PMJDY has been successful in increasing banking penetration and promoting financial inclusion across the country. The scheme has ensured access to various financial services like availability of basic savings bank account, access to need based credit, remittances facility, insurance and pension to the excluded sections i.e. weaker sections &amp; low-income groups.
- **Eligibility:** The applicant should be an Indian National. If minors above ten years apply, they will require support from their legal guardians for administering their PMJDY account.
- **Benefits/scope:** Basic Savings Bank Deposit Account (BSBDA) Any Indian citizen eligible to open a regular bank account can open a BSBDA. Such an account does not require any minimum balance maintenance. The account holders can use both bank branches, ATMs and Banking Correspondents (BCs) for depositing and withdrawing cash. However, one cannot withdraw cash more than four times a month. Small Account/Chota Khata Under Jan Dhan Yojana, people can open small bank accounts without presenting legal documents. These accounts would be valid normally for a period of twelve months. Thereafter, such accounts  would be allowed to a continue for a further period of twelve more months, if the account-holder provides a document showing that he/she has applied for any of the Officially Valid Document, within 12 months of opening the small account. RuPay Debit Card with inbuilt accident insurance Under PMJDY,  a free Rupay debit card,  with inbuilt accident insurance cover of Rs.2 lakhs (Rs 1 lakh for accounts opened before 28.08.2018),  is issued to all beneficiaries. Overdraft Facility Under PMJDY, beneficiaries can avail OD facility upto Rs. 10,000/-. Business Correspondents (BCs)/Bank Mitras  BCs/Bank Mitras are retail agents engaged by banks for providing banking services at locations other than a bank branch/ATM. It is mainly meant  for the rural areas, where bank branches are far-flung. BCs/Bank Mitras connect with the residents and guide them with banking solutions such as savings accounts, deposits, payments and withdrawals, mini account statements, etc. Banks with their strong network of BCs/Bank Mitras are providing hassle free services to the customers in remote / rural areas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2410
- **Candidate slug:** `pmagy`
- **Scheme name/title:** Pradhan Mantri Adarsh Gram Yojana
- **Details:** With a view to enabling an area-based development approach, a new scheme Pradhan Mantri Adarsh Gram Yojana (PMAGY) was launched during 2009-10. The Scheme aims at integrated development of Scheduled Castes majority villages. ﻿ The principal objective of PMAGY is the integrated development of SC majority Villages: (a) Primarily through convergent implementation of the relevant Central and State/UT Government Schemes; and (b) By taking up identified activities, which do not get covered under the existing Central and State Government Schemes, through ‘Gap-filling’ funds provided as Central Assistance to the extent of ₹20,00,000 per village. ﻿ The implementation of the Scheme was started on Pilot basis in 2009-10 and a total of 1000 villages was selected from 05 States namely Tamil Nadu (225), Rajasthan (225), Bihar (225), Himachal Pradesh (225) and Assam (100) were selected for this phase. All these 1000 villages have so far been declared as ‘Adarsh Gram’ by the respective State Governments. ﻿ The vision of an ‘Adarsh Gram' An ‘Adarsh Gram’ is one wherein people have access to various basic services so that the minimum needs of all the sections of society are fully met and disparities are reduced to a minimum. These villages would have all such infrastructure and their residents will have access to all such basic services that are necessary for a dignified living, creating thereby an environment in which everyone is enabled to utilize her/his potential to the fullest. ﻿
- **Eligibility:** Out of the villages having more than 50% SC population, only those with a total population greater than 500 will be eligible for selection in descending order of their SC population in the first instance under the Scheme. (As per the Census 2011, there are 46844 villages having more than 50% Scheduled Castes population. These villages are spread over 570 districts of 25 States &amp; UTs.) ﻿
- **Benefits/scope:** Physical Infrastructure 1.  Should be connected to the nearest major road by an all-weather road. Likewise, in the case of a multi-hamlet village, all hamlets should be connected with each other by an all-weather road. 2.  Access for all to safe drinking water on a sustainable basis. 3.  All houses should have electricity. 4.  The village should have slush-free internal roads and adequate street lighting. 5.  The village should have adequate communication facilities, such as post-office, telephones, and, if possible, internet, and Bharat Nirman Common Service Centre (being established by the Deptt. of Information Technology). 6.  Availability of adequate banking facilities through regular (brick and mortar) branches in the village or in close proximity, and through the Business Correspondent/Business Facilitator Model. 7.  All residents should have adequate housing, and there should be no homeless families. ﻿ Sanitation and Environment 1.  The village should have a high degree of sanitation- it should be free from dry latrines, and open defecation, and should have sanitary toilets, drains, and an efficient waste disposal system. It should, as far as possible, fulfill “Nirmal Gram Puraskar” norms. 2.  The Village should take care of its environment through (1) planting trees, (2) water harvest action and maintenance of water bodies (3) use of renewable sources of energy, such as biogas, solar energy, wind energy, use of smokeless chulhas, etc. ﻿ Social Infrastructure, Human Development, and Social Harmony 1.  Should have an Anganwadi center and schools of appropriate levels. 2.  The village should have adequate and attractive buildings for its Anganwadi, school, health center, panchayat, and community hall. The village should have adequate facilities for sports and other physical activities. 3.  All children in the age group of 3-6 should be enrolled in, and regularly attend the Anganwadi. Likewise, all children in the 6-14 age group should be enrolled in, and regularly attend school. 4.  All adults should be at least functionally literate and should have access to facilities for continuing education. 5.  Access for all to primary health care and Reproductive Child Health (RCH) facilities, with proper pre-natal and ante-natal care for mothers. 6.  100% institutional deliveries, full immunization of children, and observance of the small family norm. 7.  The village as a community should take special care of its women, children (especially girls), senior citizens, and persons with disabilities. 8.  There should be no public consumption of liquor or any other intoxicating substances, and their use, in general, should be discouraged. 9.  The village should have an active Gram Sabha/Gram Panchayat, women’s/swarozgaris’ Self-help Group, youth club, and Mahila Mandal. 10.  There should be no caste-based discrimination, complete eradication of untouchability, and a due sense of security and dignity among the weaker sections. 11.  Residents of the village should be aware of and exercise their constitutional and legal rights. Likewise, they should also be aware of and discharge their fundamental and civic duties. ﻿ Livelihood 1.  All youth and adults of the village should have adequate employment and means of livelihood, and there should be adequate arrangements for the development of skills among them so that as many of them as possible are in skilled employment. 2.  Progressive and efficient practices, based on new technology, should be used in all the economic activities pursued in the village, especially in agriculture, animal husbandry, fisheries, etc. 3.  Should have adequate access to remunerative prices for agricultural and other products of the village. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 13

- **Query text:** house building loan schemes
- **Original source label (unverified):** Pradhan Mantri Awas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2412
- **Candidate slug:** `pmay-u`
- **Scheme name/title:** Pradhan Mantri Awas Yojana - Urban
- **Details:** A flagship mission implemented by MoHUA, addressing urban housing shortage. The beneficiaries include Economically Weaker Section (EWS) / Low Income Group (LIG) and Middle Income Group (MIG) categories, including slum dwellers, by ensuring a pucca house to all eligible urban households by 2022. All eligible beneficiaries under all components of the scheme should have an Aadhaar/ Aadhaar Virtual ID. The Mission, as per Census 2011, covers the entire urban area consisting of Statutory Towns, Notified Planning Areas, Development Authorities, Special Area Development Authorities, Industrial Development Authorities or any such authority under State legislation which is entrusted with the functions of urban planning &amp; regulations. ﻿ The objective of the scheme is to improve the affordability of land and property amidst the continuous surge in prices. PMAY promotes and encourages sustainable and affordable housing. PMAY is a Credit Linked Subsidy Scheme (CLSS) and is also known by the name "Housing for All by 2022". Individuals availing loans to buy residential property or land or to construct homes would be eligible for interest subsidies on the said credit.
- **Eligibility:** 1. The family identifies as one of the following - a)    Economically Weaker Section (EWS): households with annual income up to ₹ 3,00,000. b)    Low Income Group (LIG): households with annual income between ₹ 3,00,001 and ₹ 6,00,000. c)    Middle Income Group-1 (MIG-1): households with annual income between ₹ 6,00,001 and ₹ 12,00,000. d)    Middle Income Group-2 (MIG-2): households with annual income between ₹ 12,00,001 and ₹ 18,00,000. 2. The applicant or his/her family members must not be owning a pucca house in any part of the country. 3. The family must comprise of husband/wife and unmarried children. 4. The town/city in which the family resides must be covered under the scheme. 5. The family MUST NOT have previously availed the benefits of any housing-related schemes set up by the Government of India.
- **Benefits/scope:** Slum rehabilitation of eligible Slum Dwellers with participation of private developers using land as a resource. Promotion of Affordable Housing through Credit Linked Subsidy Scheme (CLSS). EWS: Annual Household Income up to Rs.3,00,000; house sizes upto 30 sq.m;   LIG: Annual Household Income from Rs.3,00,001 to Rs.6,00,000; house sizes upto 60 sq.m;    MIG I: Annual Household Income from Rs. 6,00,001 to Rs. 12,00,000; house sizes upto 160 sq.m;    MIG II: Annual Household Income from Rs.12,00,001 and 18,00,000; house sizes upto 200 sq.m Affordable Housing in Partnership with Public &amp; Private sectors: Central Assistance per EWS house in projects where 35% of houses are for EWSs Subsidy for Beneficiary-Led individual house construction /enhancement: For individuals of EWS category requiring individual house (separate project for such beneficiaries)
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2411
- **Candidate slug:** `pmay-g`
- **Scheme name/title:** Pradhan Mantri Awaas Yojana - Gramin
- **Details:** Launch on 1st April 2016, Pradhan Mantri Awaas Yojana Gramin (PMAY-G) is centre's flagship mission by the Ministry of Rural Development (MoRD), implemented by the Ministry of Housing and Urban Affairs (MoHUA). PMAY-G aims at providing a pucca house, with basic amenities, to all houseless households and those households living in kutcha and dilapidated house. PMAY-G addresses the rural housing shortage and bridges the housing deficit in rural areas of India, contributing significantly to the mission of "Housing for All". The minimum size of the houses under PMAY-G is 25 sq m including a dedicated area for hygienic cooking. As of 27th Sept 2022, 2.00 crore houses have been constructed out of the total target of 2.72 crores. The beneficiaries are identified using the Socio-Economic and Caste Census (SECC) parameters and verified by the Gram Sabhas. The amount is transferred directly to the Aadhaar-Linked Bank Account / Post-Office Account of the beneficiary. PMAY-G has been extended for another two years, i.e. till 31st March 2024. Aim and Objective: PMAY-G aims to provide a pucca house with basic amenities to all houseless households and households living in kutcha and dilapidated house in rural areas by 2024. The immediate objective is to cover 1.00 Crore households in rural areas, that are houseless or living in kutcha / dilapidated house, in three years from 2016-17 to 2018-19 and enable construction of quality houses by the beneficiaries using local materials, designs and trained masons. For houses to become homes, adoption of a habitat approach through convergence is proposed.
- **Eligibility:** The universe of eligible beneficiaries under PMAY-G will include all the houseless households living in zero, one, or two-room houses with kutcha walls and kutcha roofs (as per SECC data, and subject to the exclusion process). Criteria for Automatic/Compulsory Inclusion -  1.	Households without shelter 2.	Destitute/ living on alms 3.	Manual scavengers 4.	Primitive Tribal Groups 5.	Legally released bonded laborer Prioritisation within the Universe i.  There will be multilayered prioritization within the universe of eligible PMAY-G beneficiaries. Priority will first be assigned on the basis of parameters reflecting housing deprivation in each category viz., SC/ST, Minorities, and Others. ii.  To begin with, households will be prioritized based on houselessness followed by the number of rooms; zero, one, and two rooms, in that order. iii.  In a particular social category viz., SC/ST, Minorities, and Others, households that are houseless or living in houses with a lower number of rooms shall not be ranked below households living in houses with a higher number of rooms. Within the above priority groups, households that fulfill the criteria of "compulsory inclusion", will be further elevated. Automatically included households shall not rank lower than other households within a priority group. Inter-se priority within the two subgroups viz. households which are automatically included and otherwise will be determined based on their cumulative deprivation scores. The scores will be calculated from the socio-economic parameters given below with each having equal weight: i.	Households with no adult member between ages 16 to 59 ii.	Female-headed households with no adult male member between ages 16 to 59 iii.	Households with no literate adult above 25 years iv.	Households with any disabled member and no able-bodied adult member v.	Landless Households deriving the major part of their income from manual casual labor vi. Households with higher deprivation scores will be ranked higher within the subgroups. Note:  To ensure that assistance is targeted at those who are genuinely deprived and that the selection is objective and verifiable, the housing deprivation parameters in the SECC data will be used for identifying households and then verified by the Gram Sabhas. Earmarking of Targets - For SC/ST: 60% of the target allocated to each State/ UT should be earmarked for SC/STs, subject to the availability of eligible beneficiaries. Within earmarked targets, the proportion of SC and ST is to be decided from time to time by the respective States/UTs. Further, the States/ UTs would be allowed to interchange targets between SC and ST if there are no eligible beneficiaries from either of the category and it is certified as such. In case all eligible SC and ST households are covered, the State/ UT targets would be allocated to beneficiaries from the 'Other' categories included in the Permanent Wait List drawn from SECC 2011. For Minorities: Further, as far as possible, 15% of the total fund would be earmarked for Minorities at the National Level for households. The allocation of targets for Minorities among the States/UTs will be on the basis of the proportionate rural population of Minorities in the respective State/UT as per Census 2011 data. Minorities notified under Section 2(c) of the National Commission for Minorities Act, 1992 are to be considered eligible for receiving benefits against Minority earmarks. For PwDs: Accordingly, in the scheme of PMAY-G, while deciding the inter-se priority among the beneficiaries who are to be provided assistance, households with any disabled member and no able-bodied adult member have been accorded additional deprivation score so that such households are given priority while allotting the houses. Keeping in view the provisions of the Persons with Disabilities Act, of 1995, the States to the extent possible, may ensure that 3% of beneficiaries at the State Level are from among persons with disabilities. Tie Breaker In case there is a tie with more than one household within a subgroup having the same deprivation score, the households will be ranked according to priority on the basis of the following parameters: i.	Households with widows and next-of-kin of members of defence/paramilitary/police forces killed in action. ii.	Households where a member is suffering from leprosy or cancer and People living with HIV (PLHIV). iii.	Households with a single girl child. iv.	Beneficiary families of the Scheduled Tribes and Other Traditional Forest Dwellers (Recognition of Forest Rights) Act, 2006, commonly known as the Forest Rights Act. v.	Transgender persons.
- **Benefits/scope:** Financial Assistance of ₹ 1,20,000 per unit for plain areas; and ₹ 1,30,000 per unit for hilly areas, difficult areas, and IAP districts (Himalayan states, North-Eastern states, and Union Territories of Jammu &amp; Kashmir). A willing beneficiary can avail of institutional finance (loan) of up to ₹ 70,000 at 3% lower interest rate, to build a permanent house. The maximum principal amount for which subsidy can be sought is ₹ 2,00,000. The minimum size of the house shall be is 25 sq m including a dedicated area for hygienic cooking. In convergence with Swachh Bharat Mission-Gramin (SBM-G), the beneficiaries get financial assistance of up to ₹ 12,000 for the construction of toilets. In convergence with MGNREGA, the beneficiary is entitled to employment as unskilled labor (Rural Mason Training) at ₹ 90.95 per day for 95 days. In convergence with Pradhan Mantri Ujjwala Yojana, one LPG connection per house is provided. Convergence with different government programmes for piped drinking water, electricity connection, clean &amp; efficient cooking fuel, treatment of social and liquid waste, etc. Payments are made electronically directly to bank accounts or post office accounts that are linked to Aadhaar. Note: Beneficiaries are identified using the "Housing Deprivation Parameters" from the Socio-Economic and Caste Census (SECC) 2011 [ https://secc.gov.in/] , further verified by the Gram Sabhas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 14

- **Query text:** affordable housing scheme
- **Original source label (unverified):** Pradhan Mantri Awas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2412
- **Candidate slug:** `pmay-u`
- **Scheme name/title:** Pradhan Mantri Awas Yojana - Urban
- **Details:** A flagship mission implemented by MoHUA, addressing urban housing shortage. The beneficiaries include Economically Weaker Section (EWS) / Low Income Group (LIG) and Middle Income Group (MIG) categories, including slum dwellers, by ensuring a pucca house to all eligible urban households by 2022. All eligible beneficiaries under all components of the scheme should have an Aadhaar/ Aadhaar Virtual ID. The Mission, as per Census 2011, covers the entire urban area consisting of Statutory Towns, Notified Planning Areas, Development Authorities, Special Area Development Authorities, Industrial Development Authorities or any such authority under State legislation which is entrusted with the functions of urban planning &amp; regulations. ﻿ The objective of the scheme is to improve the affordability of land and property amidst the continuous surge in prices. PMAY promotes and encourages sustainable and affordable housing. PMAY is a Credit Linked Subsidy Scheme (CLSS) and is also known by the name "Housing for All by 2022". Individuals availing loans to buy residential property or land or to construct homes would be eligible for interest subsidies on the said credit.
- **Eligibility:** 1. The family identifies as one of the following - a)    Economically Weaker Section (EWS): households with annual income up to ₹ 3,00,000. b)    Low Income Group (LIG): households with annual income between ₹ 3,00,001 and ₹ 6,00,000. c)    Middle Income Group-1 (MIG-1): households with annual income between ₹ 6,00,001 and ₹ 12,00,000. d)    Middle Income Group-2 (MIG-2): households with annual income between ₹ 12,00,001 and ₹ 18,00,000. 2. The applicant or his/her family members must not be owning a pucca house in any part of the country. 3. The family must comprise of husband/wife and unmarried children. 4. The town/city in which the family resides must be covered under the scheme. 5. The family MUST NOT have previously availed the benefits of any housing-related schemes set up by the Government of India.
- **Benefits/scope:** Slum rehabilitation of eligible Slum Dwellers with participation of private developers using land as a resource. Promotion of Affordable Housing through Credit Linked Subsidy Scheme (CLSS). EWS: Annual Household Income up to Rs.3,00,000; house sizes upto 30 sq.m;   LIG: Annual Household Income from Rs.3,00,001 to Rs.6,00,000; house sizes upto 60 sq.m;    MIG I: Annual Household Income from Rs. 6,00,001 to Rs. 12,00,000; house sizes upto 160 sq.m;    MIG II: Annual Household Income from Rs.12,00,001 and 18,00,000; house sizes upto 200 sq.m Affordable Housing in Partnership with Public &amp; Private sectors: Central Assistance per EWS house in projects where 35% of houses are for EWSs Subsidy for Beneficiary-Led individual house construction /enhancement: For individuals of EWS category requiring individual house (separate project for such beneficiaries)
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2411
- **Candidate slug:** `pmay-g`
- **Scheme name/title:** Pradhan Mantri Awaas Yojana - Gramin
- **Details:** Launch on 1st April 2016, Pradhan Mantri Awaas Yojana Gramin (PMAY-G) is centre's flagship mission by the Ministry of Rural Development (MoRD), implemented by the Ministry of Housing and Urban Affairs (MoHUA). PMAY-G aims at providing a pucca house, with basic amenities, to all houseless households and those households living in kutcha and dilapidated house. PMAY-G addresses the rural housing shortage and bridges the housing deficit in rural areas of India, contributing significantly to the mission of "Housing for All". The minimum size of the houses under PMAY-G is 25 sq m including a dedicated area for hygienic cooking. As of 27th Sept 2022, 2.00 crore houses have been constructed out of the total target of 2.72 crores. The beneficiaries are identified using the Socio-Economic and Caste Census (SECC) parameters and verified by the Gram Sabhas. The amount is transferred directly to the Aadhaar-Linked Bank Account / Post-Office Account of the beneficiary. PMAY-G has been extended for another two years, i.e. till 31st March 2024. Aim and Objective: PMAY-G aims to provide a pucca house with basic amenities to all houseless households and households living in kutcha and dilapidated house in rural areas by 2024. The immediate objective is to cover 1.00 Crore households in rural areas, that are houseless or living in kutcha / dilapidated house, in three years from 2016-17 to 2018-19 and enable construction of quality houses by the beneficiaries using local materials, designs and trained masons. For houses to become homes, adoption of a habitat approach through convergence is proposed.
- **Eligibility:** The universe of eligible beneficiaries under PMAY-G will include all the houseless households living in zero, one, or two-room houses with kutcha walls and kutcha roofs (as per SECC data, and subject to the exclusion process). Criteria for Automatic/Compulsory Inclusion -  1.	Households without shelter 2.	Destitute/ living on alms 3.	Manual scavengers 4.	Primitive Tribal Groups 5.	Legally released bonded laborer Prioritisation within the Universe i.  There will be multilayered prioritization within the universe of eligible PMAY-G beneficiaries. Priority will first be assigned on the basis of parameters reflecting housing deprivation in each category viz., SC/ST, Minorities, and Others. ii.  To begin with, households will be prioritized based on houselessness followed by the number of rooms; zero, one, and two rooms, in that order. iii.  In a particular social category viz., SC/ST, Minorities, and Others, households that are houseless or living in houses with a lower number of rooms shall not be ranked below households living in houses with a higher number of rooms. Within the above priority groups, households that fulfill the criteria of "compulsory inclusion", will be further elevated. Automatically included households shall not rank lower than other households within a priority group. Inter-se priority within the two subgroups viz. households which are automatically included and otherwise will be determined based on their cumulative deprivation scores. The scores will be calculated from the socio-economic parameters given below with each having equal weight: i.	Households with no adult member between ages 16 to 59 ii.	Female-headed households with no adult male member between ages 16 to 59 iii.	Households with no literate adult above 25 years iv.	Households with any disabled member and no able-bodied adult member v.	Landless Households deriving the major part of their income from manual casual labor vi. Households with higher deprivation scores will be ranked higher within the subgroups. Note:  To ensure that assistance is targeted at those who are genuinely deprived and that the selection is objective and verifiable, the housing deprivation parameters in the SECC data will be used for identifying households and then verified by the Gram Sabhas. Earmarking of Targets - For SC/ST: 60% of the target allocated to each State/ UT should be earmarked for SC/STs, subject to the availability of eligible beneficiaries. Within earmarked targets, the proportion of SC and ST is to be decided from time to time by the respective States/UTs. Further, the States/ UTs would be allowed to interchange targets between SC and ST if there are no eligible beneficiaries from either of the category and it is certified as such. In case all eligible SC and ST households are covered, the State/ UT targets would be allocated to beneficiaries from the 'Other' categories included in the Permanent Wait List drawn from SECC 2011. For Minorities: Further, as far as possible, 15% of the total fund would be earmarked for Minorities at the National Level for households. The allocation of targets for Minorities among the States/UTs will be on the basis of the proportionate rural population of Minorities in the respective State/UT as per Census 2011 data. Minorities notified under Section 2(c) of the National Commission for Minorities Act, 1992 are to be considered eligible for receiving benefits against Minority earmarks. For PwDs: Accordingly, in the scheme of PMAY-G, while deciding the inter-se priority among the beneficiaries who are to be provided assistance, households with any disabled member and no able-bodied adult member have been accorded additional deprivation score so that such households are given priority while allotting the houses. Keeping in view the provisions of the Persons with Disabilities Act, of 1995, the States to the extent possible, may ensure that 3% of beneficiaries at the State Level are from among persons with disabilities. Tie Breaker In case there is a tie with more than one household within a subgroup having the same deprivation score, the households will be ranked according to priority on the basis of the following parameters: i.	Households with widows and next-of-kin of members of defence/paramilitary/police forces killed in action. ii.	Households where a member is suffering from leprosy or cancer and People living with HIV (PLHIV). iii.	Households with a single girl child. iv.	Beneficiary families of the Scheduled Tribes and Other Traditional Forest Dwellers (Recognition of Forest Rights) Act, 2006, commonly known as the Forest Rights Act. v.	Transgender persons.
- **Benefits/scope:** Financial Assistance of ₹ 1,20,000 per unit for plain areas; and ₹ 1,30,000 per unit for hilly areas, difficult areas, and IAP districts (Himalayan states, North-Eastern states, and Union Territories of Jammu &amp; Kashmir). A willing beneficiary can avail of institutional finance (loan) of up to ₹ 70,000 at 3% lower interest rate, to build a permanent house. The maximum principal amount for which subsidy can be sought is ₹ 2,00,000. The minimum size of the house shall be is 25 sq m including a dedicated area for hygienic cooking. In convergence with Swachh Bharat Mission-Gramin (SBM-G), the beneficiaries get financial assistance of up to ₹ 12,000 for the construction of toilets. In convergence with MGNREGA, the beneficiary is entitled to employment as unskilled labor (Rural Mason Training) at ₹ 90.95 per day for 95 days. In convergence with Pradhan Mantri Ujjwala Yojana, one LPG connection per house is provided. Convergence with different government programmes for piped drinking water, electricity connection, clean &amp; efficient cooking fuel, treatment of social and liquid waste, etc. Payments are made electronically directly to bank accounts or post office accounts that are linked to Aadhaar. Note: Beneficiaries are identified using the "Housing Deprivation Parameters" from the Socio-Economic and Caste Census (SECC) 2011 [ https://secc.gov.in/] , further verified by the Gram Sabhas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 15

- **Query text:** home construction assistance
- **Original source label (unverified):** Pradhan Mantri Awas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2412
- **Candidate slug:** `pmay-u`
- **Scheme name/title:** Pradhan Mantri Awas Yojana - Urban
- **Details:** A flagship mission implemented by MoHUA, addressing urban housing shortage. The beneficiaries include Economically Weaker Section (EWS) / Low Income Group (LIG) and Middle Income Group (MIG) categories, including slum dwellers, by ensuring a pucca house to all eligible urban households by 2022. All eligible beneficiaries under all components of the scheme should have an Aadhaar/ Aadhaar Virtual ID. The Mission, as per Census 2011, covers the entire urban area consisting of Statutory Towns, Notified Planning Areas, Development Authorities, Special Area Development Authorities, Industrial Development Authorities or any such authority under State legislation which is entrusted with the functions of urban planning &amp; regulations. ﻿ The objective of the scheme is to improve the affordability of land and property amidst the continuous surge in prices. PMAY promotes and encourages sustainable and affordable housing. PMAY is a Credit Linked Subsidy Scheme (CLSS) and is also known by the name "Housing for All by 2022". Individuals availing loans to buy residential property or land or to construct homes would be eligible for interest subsidies on the said credit.
- **Eligibility:** 1. The family identifies as one of the following - a)    Economically Weaker Section (EWS): households with annual income up to ₹ 3,00,000. b)    Low Income Group (LIG): households with annual income between ₹ 3,00,001 and ₹ 6,00,000. c)    Middle Income Group-1 (MIG-1): households with annual income between ₹ 6,00,001 and ₹ 12,00,000. d)    Middle Income Group-2 (MIG-2): households with annual income between ₹ 12,00,001 and ₹ 18,00,000. 2. The applicant or his/her family members must not be owning a pucca house in any part of the country. 3. The family must comprise of husband/wife and unmarried children. 4. The town/city in which the family resides must be covered under the scheme. 5. The family MUST NOT have previously availed the benefits of any housing-related schemes set up by the Government of India.
- **Benefits/scope:** Slum rehabilitation of eligible Slum Dwellers with participation of private developers using land as a resource. Promotion of Affordable Housing through Credit Linked Subsidy Scheme (CLSS). EWS: Annual Household Income up to Rs.3,00,000; house sizes upto 30 sq.m;   LIG: Annual Household Income from Rs.3,00,001 to Rs.6,00,000; house sizes upto 60 sq.m;    MIG I: Annual Household Income from Rs. 6,00,001 to Rs. 12,00,000; house sizes upto 160 sq.m;    MIG II: Annual Household Income from Rs.12,00,001 and 18,00,000; house sizes upto 200 sq.m Affordable Housing in Partnership with Public &amp; Private sectors: Central Assistance per EWS house in projects where 35% of houses are for EWSs Subsidy for Beneficiary-Led individual house construction /enhancement: For individuals of EWS category requiring individual house (separate project for such beneficiaries)
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2411
- **Candidate slug:** `pmay-g`
- **Scheme name/title:** Pradhan Mantri Awaas Yojana - Gramin
- **Details:** Launch on 1st April 2016, Pradhan Mantri Awaas Yojana Gramin (PMAY-G) is centre's flagship mission by the Ministry of Rural Development (MoRD), implemented by the Ministry of Housing and Urban Affairs (MoHUA). PMAY-G aims at providing a pucca house, with basic amenities, to all houseless households and those households living in kutcha and dilapidated house. PMAY-G addresses the rural housing shortage and bridges the housing deficit in rural areas of India, contributing significantly to the mission of "Housing for All". The minimum size of the houses under PMAY-G is 25 sq m including a dedicated area for hygienic cooking. As of 27th Sept 2022, 2.00 crore houses have been constructed out of the total target of 2.72 crores. The beneficiaries are identified using the Socio-Economic and Caste Census (SECC) parameters and verified by the Gram Sabhas. The amount is transferred directly to the Aadhaar-Linked Bank Account / Post-Office Account of the beneficiary. PMAY-G has been extended for another two years, i.e. till 31st March 2024. Aim and Objective: PMAY-G aims to provide a pucca house with basic amenities to all houseless households and households living in kutcha and dilapidated house in rural areas by 2024. The immediate objective is to cover 1.00 Crore households in rural areas, that are houseless or living in kutcha / dilapidated house, in three years from 2016-17 to 2018-19 and enable construction of quality houses by the beneficiaries using local materials, designs and trained masons. For houses to become homes, adoption of a habitat approach through convergence is proposed.
- **Eligibility:** The universe of eligible beneficiaries under PMAY-G will include all the houseless households living in zero, one, or two-room houses with kutcha walls and kutcha roofs (as per SECC data, and subject to the exclusion process). Criteria for Automatic/Compulsory Inclusion -  1.	Households without shelter 2.	Destitute/ living on alms 3.	Manual scavengers 4.	Primitive Tribal Groups 5.	Legally released bonded laborer Prioritisation within the Universe i.  There will be multilayered prioritization within the universe of eligible PMAY-G beneficiaries. Priority will first be assigned on the basis of parameters reflecting housing deprivation in each category viz., SC/ST, Minorities, and Others. ii.  To begin with, households will be prioritized based on houselessness followed by the number of rooms; zero, one, and two rooms, in that order. iii.  In a particular social category viz., SC/ST, Minorities, and Others, households that are houseless or living in houses with a lower number of rooms shall not be ranked below households living in houses with a higher number of rooms. Within the above priority groups, households that fulfill the criteria of "compulsory inclusion", will be further elevated. Automatically included households shall not rank lower than other households within a priority group. Inter-se priority within the two subgroups viz. households which are automatically included and otherwise will be determined based on their cumulative deprivation scores. The scores will be calculated from the socio-economic parameters given below with each having equal weight: i.	Households with no adult member between ages 16 to 59 ii.	Female-headed households with no adult male member between ages 16 to 59 iii.	Households with no literate adult above 25 years iv.	Households with any disabled member and no able-bodied adult member v.	Landless Households deriving the major part of their income from manual casual labor vi. Households with higher deprivation scores will be ranked higher within the subgroups. Note:  To ensure that assistance is targeted at those who are genuinely deprived and that the selection is objective and verifiable, the housing deprivation parameters in the SECC data will be used for identifying households and then verified by the Gram Sabhas. Earmarking of Targets - For SC/ST: 60% of the target allocated to each State/ UT should be earmarked for SC/STs, subject to the availability of eligible beneficiaries. Within earmarked targets, the proportion of SC and ST is to be decided from time to time by the respective States/UTs. Further, the States/ UTs would be allowed to interchange targets between SC and ST if there are no eligible beneficiaries from either of the category and it is certified as such. In case all eligible SC and ST households are covered, the State/ UT targets would be allocated to beneficiaries from the 'Other' categories included in the Permanent Wait List drawn from SECC 2011. For Minorities: Further, as far as possible, 15% of the total fund would be earmarked for Minorities at the National Level for households. The allocation of targets for Minorities among the States/UTs will be on the basis of the proportionate rural population of Minorities in the respective State/UT as per Census 2011 data. Minorities notified under Section 2(c) of the National Commission for Minorities Act, 1992 are to be considered eligible for receiving benefits against Minority earmarks. For PwDs: Accordingly, in the scheme of PMAY-G, while deciding the inter-se priority among the beneficiaries who are to be provided assistance, households with any disabled member and no able-bodied adult member have been accorded additional deprivation score so that such households are given priority while allotting the houses. Keeping in view the provisions of the Persons with Disabilities Act, of 1995, the States to the extent possible, may ensure that 3% of beneficiaries at the State Level are from among persons with disabilities. Tie Breaker In case there is a tie with more than one household within a subgroup having the same deprivation score, the households will be ranked according to priority on the basis of the following parameters: i.	Households with widows and next-of-kin of members of defence/paramilitary/police forces killed in action. ii.	Households where a member is suffering from leprosy or cancer and People living with HIV (PLHIV). iii.	Households with a single girl child. iv.	Beneficiary families of the Scheduled Tribes and Other Traditional Forest Dwellers (Recognition of Forest Rights) Act, 2006, commonly known as the Forest Rights Act. v.	Transgender persons.
- **Benefits/scope:** Financial Assistance of ₹ 1,20,000 per unit for plain areas; and ₹ 1,30,000 per unit for hilly areas, difficult areas, and IAP districts (Himalayan states, North-Eastern states, and Union Territories of Jammu &amp; Kashmir). A willing beneficiary can avail of institutional finance (loan) of up to ₹ 70,000 at 3% lower interest rate, to build a permanent house. The maximum principal amount for which subsidy can be sought is ₹ 2,00,000. The minimum size of the house shall be is 25 sq m including a dedicated area for hygienic cooking. In convergence with Swachh Bharat Mission-Gramin (SBM-G), the beneficiaries get financial assistance of up to ₹ 12,000 for the construction of toilets. In convergence with MGNREGA, the beneficiary is entitled to employment as unskilled labor (Rural Mason Training) at ₹ 90.95 per day for 95 days. In convergence with Pradhan Mantri Ujjwala Yojana, one LPG connection per house is provided. Convergence with different government programmes for piped drinking water, electricity connection, clean &amp; efficient cooking fuel, treatment of social and liquid waste, etc. Payments are made electronically directly to bank accounts or post office accounts that are linked to Aadhaar. Note: Beneficiaries are identified using the "Housing Deprivation Parameters" from the Socio-Economic and Caste Census (SECC) 2011 [ https://secc.gov.in/] , further verified by the Gram Sabhas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 16

- **Query text:** girl child education support
- **Original source label (unverified):** Sukanya Samriddhi Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1771
- **Candidate slug:** `cbssc-msy`
- **Scheme name/title:** Mahila Samriddhi Yojana
- **Details:** Mahila Samridhi Yojana (MSY) is a scheme aimed to benefit women entrepreneurs from backward backgrounds or poor backgrounds. The scheme was launched as part of the National Backward Classes Finance and Development Corporation (NBCFDC) under the Ministry of Social Justice and Empowerment. Under this scheme, the Corporation bears the training cost and stipend for training that is provided to groups of about 20 women, in suitable craft activities. The group is formed into a SHG and after the training, micro-credit is provided. This scheme is being implemented by a wide range of channel partners nationwide. Targeted women beneficiaries are identified and given loans either directly or in the form of Self-Help Groups (SHGs). The two main targeted beneficiaries are: Self-help groups (SHGs): It aims to strengthen and assist SHGs, particularly those that include women. These people make up the autonomous, economically disadvantaged category. Women belonging to economically and socially backward classes (targeted groups): Women from the underprivileged classes are considered, particularly those who fall under the SC or ST category. Objectives of Mahila Samridhi Yojana To encourage women belonging to minority groups from rural regions and underprivileged classes to adopt an entrepreneurial attitude. To help these women meet their entrepreneurial goals by providing microfinance loans at lower interest rates. To encourage women from scheduled castes or scheduled tribes or any other minority populations to pursue their aspirations. To encourage women to overcome social stigma and gain financial independence. To assist women who are unable to establish their own businesses or careers owing to a lack of financial assistance. It is also a Micro Finance Scheme for women with rebate in interest.
- **Eligibility:** Applicant must be between 18 to 55 years of age. Applicable to Women from low-income families or women who belong to SC/ST/OBC categories as notified by the Central/State Government and whose family income is less than Rupees three lakhs per annum. Applicable to Women looking to start their own business or engage in income-generating activities.
- **Benefits/scope:** It is a microfinance scheme for women with a rebate in interest. Financial Assistance up to the cost of Rs. 1,40,000/- is provided. The repayment period is within 3.5 years, in quarterly installments from the date of each disbursement including the moratorium period. On repayment of loans under MSY, through the concerned State Channelizing Agencies (SCA), the eligible beneficiaries can avail of any loan under the NSFDC scheme.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 366
- **Candidate slug:** `bsy-pudu`
- **Scheme name/title:** Balika Samrithi Yojana
- **Details:** The scheme “Balika Samrithi Yojana” by the Department of Women &amp; Child Development, Government of Pondicherry was introduced to improve the status of the girl child and provide nutritious food to the girl child. Through this scheme, assistance of ₹500 in the form of a National Savings Certificate is provided to lactating mothers. The target beneficiaries are girl children born on or after 15-8-97.
- **Eligibility:** The applicant should be a girl child born on or after 15-8-97. The annual income of the family of the applicant should not exceed ₹15,000. The applicant should be a citizen of India. The applicant should be a native of the Union Territory of Pondicherry by birth or continuous residence for not less than 3 years.
- **Benefits/scope:** Assistance of ₹500 in the form of a National Savings Certificate.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2923
- **Candidate slug:** `ssyh`
- **Scheme name/title:** Shilpi Samridhi Yojana
- **Details:** "Shilpi Samridhi Yojana" is an economic empowerment scheme by the Haryana Scheduled Castes Finance and Development Corporation, Government of Haryana. Through this scheme, loans/benefits are provided to the eligible families of the scheduled caste artisans to pursue various economic development activities for the betterment of their economic status. In order to be eligible, the artisan should be in the age group of 18 to 45 years. He/She should not be a defaulter of the Corporation/bank.
- **Eligibility:** The applicant should be a permanent resident of Haryana. The applicant should belong to the Scheduled Caste category. The applicant's annual family income should not exceed ₹3,00,000/-. The applicant should be in the age group of 18 to 45 years. The applicant should have adequate knowledge and experience of the scheme. The applicant should not have misused the previous loan obtained from the Corporation. The applicant should not have any other similar unit. The applicant should not be a defaulter of the Corporation/banks.
- **Benefits/scope:** Loan for various economic development schemes having unit cost up to ₹50,000/-. Margin Money at 10% of the project cost. Subsidy at 50% of the total project cost, subject to a maximum of ₹10,000/-.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 17

- **Query text:** savings scheme for daughters
- **Original source label (unverified):** Sukanya Samriddhi Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1771
- **Candidate slug:** `cbssc-msy`
- **Scheme name/title:** Mahila Samriddhi Yojana
- **Details:** Mahila Samridhi Yojana (MSY) is a scheme aimed to benefit women entrepreneurs from backward backgrounds or poor backgrounds. The scheme was launched as part of the National Backward Classes Finance and Development Corporation (NBCFDC) under the Ministry of Social Justice and Empowerment. Under this scheme, the Corporation bears the training cost and stipend for training that is provided to groups of about 20 women, in suitable craft activities. The group is formed into a SHG and after the training, micro-credit is provided. This scheme is being implemented by a wide range of channel partners nationwide. Targeted women beneficiaries are identified and given loans either directly or in the form of Self-Help Groups (SHGs). The two main targeted beneficiaries are: Self-help groups (SHGs): It aims to strengthen and assist SHGs, particularly those that include women. These people make up the autonomous, economically disadvantaged category. Women belonging to economically and socially backward classes (targeted groups): Women from the underprivileged classes are considered, particularly those who fall under the SC or ST category. Objectives of Mahila Samridhi Yojana To encourage women belonging to minority groups from rural regions and underprivileged classes to adopt an entrepreneurial attitude. To help these women meet their entrepreneurial goals by providing microfinance loans at lower interest rates. To encourage women from scheduled castes or scheduled tribes or any other minority populations to pursue their aspirations. To encourage women to overcome social stigma and gain financial independence. To assist women who are unable to establish their own businesses or careers owing to a lack of financial assistance. It is also a Micro Finance Scheme for women with rebate in interest.
- **Eligibility:** Applicant must be between 18 to 55 years of age. Applicable to Women from low-income families or women who belong to SC/ST/OBC categories as notified by the Central/State Government and whose family income is less than Rupees three lakhs per annum. Applicable to Women looking to start their own business or engage in income-generating activities.
- **Benefits/scope:** It is a microfinance scheme for women with a rebate in interest. Financial Assistance up to the cost of Rs. 1,40,000/- is provided. The repayment period is within 3.5 years, in quarterly installments from the date of each disbursement including the moratorium period. On repayment of loans under MSY, through the concerned State Channelizing Agencies (SCA), the eligible beneficiaries can avail of any loan under the NSFDC scheme.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 366
- **Candidate slug:** `bsy-pudu`
- **Scheme name/title:** Balika Samrithi Yojana
- **Details:** The scheme “Balika Samrithi Yojana” by the Department of Women &amp; Child Development, Government of Pondicherry was introduced to improve the status of the girl child and provide nutritious food to the girl child. Through this scheme, assistance of ₹500 in the form of a National Savings Certificate is provided to lactating mothers. The target beneficiaries are girl children born on or after 15-8-97.
- **Eligibility:** The applicant should be a girl child born on or after 15-8-97. The annual income of the family of the applicant should not exceed ₹15,000. The applicant should be a citizen of India. The applicant should be a native of the Union Territory of Pondicherry by birth or continuous residence for not less than 3 years.
- **Benefits/scope:** Assistance of ₹500 in the form of a National Savings Certificate.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2923
- **Candidate slug:** `ssyh`
- **Scheme name/title:** Shilpi Samridhi Yojana
- **Details:** "Shilpi Samridhi Yojana" is an economic empowerment scheme by the Haryana Scheduled Castes Finance and Development Corporation, Government of Haryana. Through this scheme, loans/benefits are provided to the eligible families of the scheduled caste artisans to pursue various economic development activities for the betterment of their economic status. In order to be eligible, the artisan should be in the age group of 18 to 45 years. He/She should not be a defaulter of the Corporation/bank.
- **Eligibility:** The applicant should be a permanent resident of Haryana. The applicant should belong to the Scheduled Caste category. The applicant's annual family income should not exceed ₹3,00,000/-. The applicant should be in the age group of 18 to 45 years. The applicant should have adequate knowledge and experience of the scheme. The applicant should not have misused the previous loan obtained from the Corporation. The applicant should not have any other similar unit. The applicant should not be a defaulter of the Corporation/banks.
- **Benefits/scope:** Loan for various economic development schemes having unit cost up to ₹50,000/-. Margin Money at 10% of the project cost. Subsidy at 50% of the total project cost, subject to a maximum of ₹10,000/-.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 18

- **Query text:** female child financial security
- **Original source label (unverified):** Sukanya Samriddhi Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1771
- **Candidate slug:** `cbssc-msy`
- **Scheme name/title:** Mahila Samriddhi Yojana
- **Details:** Mahila Samridhi Yojana (MSY) is a scheme aimed to benefit women entrepreneurs from backward backgrounds or poor backgrounds. The scheme was launched as part of the National Backward Classes Finance and Development Corporation (NBCFDC) under the Ministry of Social Justice and Empowerment. Under this scheme, the Corporation bears the training cost and stipend for training that is provided to groups of about 20 women, in suitable craft activities. The group is formed into a SHG and after the training, micro-credit is provided. This scheme is being implemented by a wide range of channel partners nationwide. Targeted women beneficiaries are identified and given loans either directly or in the form of Self-Help Groups (SHGs). The two main targeted beneficiaries are: Self-help groups (SHGs): It aims to strengthen and assist SHGs, particularly those that include women. These people make up the autonomous, economically disadvantaged category. Women belonging to economically and socially backward classes (targeted groups): Women from the underprivileged classes are considered, particularly those who fall under the SC or ST category. Objectives of Mahila Samridhi Yojana To encourage women belonging to minority groups from rural regions and underprivileged classes to adopt an entrepreneurial attitude. To help these women meet their entrepreneurial goals by providing microfinance loans at lower interest rates. To encourage women from scheduled castes or scheduled tribes or any other minority populations to pursue their aspirations. To encourage women to overcome social stigma and gain financial independence. To assist women who are unable to establish their own businesses or careers owing to a lack of financial assistance. It is also a Micro Finance Scheme for women with rebate in interest.
- **Eligibility:** Applicant must be between 18 to 55 years of age. Applicable to Women from low-income families or women who belong to SC/ST/OBC categories as notified by the Central/State Government and whose family income is less than Rupees three lakhs per annum. Applicable to Women looking to start their own business or engage in income-generating activities.
- **Benefits/scope:** It is a microfinance scheme for women with a rebate in interest. Financial Assistance up to the cost of Rs. 1,40,000/- is provided. The repayment period is within 3.5 years, in quarterly installments from the date of each disbursement including the moratorium period. On repayment of loans under MSY, through the concerned State Channelizing Agencies (SCA), the eligible beneficiaries can avail of any loan under the NSFDC scheme.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 366
- **Candidate slug:** `bsy-pudu`
- **Scheme name/title:** Balika Samrithi Yojana
- **Details:** The scheme “Balika Samrithi Yojana” by the Department of Women &amp; Child Development, Government of Pondicherry was introduced to improve the status of the girl child and provide nutritious food to the girl child. Through this scheme, assistance of ₹500 in the form of a National Savings Certificate is provided to lactating mothers. The target beneficiaries are girl children born on or after 15-8-97.
- **Eligibility:** The applicant should be a girl child born on or after 15-8-97. The annual income of the family of the applicant should not exceed ₹15,000. The applicant should be a citizen of India. The applicant should be a native of the Union Territory of Pondicherry by birth or continuous residence for not less than 3 years.
- **Benefits/scope:** Assistance of ₹500 in the form of a National Savings Certificate.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2923
- **Candidate slug:** `ssyh`
- **Scheme name/title:** Shilpi Samridhi Yojana
- **Details:** "Shilpi Samridhi Yojana" is an economic empowerment scheme by the Haryana Scheduled Castes Finance and Development Corporation, Government of Haryana. Through this scheme, loans/benefits are provided to the eligible families of the scheduled caste artisans to pursue various economic development activities for the betterment of their economic status. In order to be eligible, the artisan should be in the age group of 18 to 45 years. He/She should not be a defaulter of the Corporation/bank.
- **Eligibility:** The applicant should be a permanent resident of Haryana. The applicant should belong to the Scheduled Caste category. The applicant's annual family income should not exceed ₹3,00,000/-. The applicant should be in the age group of 18 to 45 years. The applicant should have adequate knowledge and experience of the scheme. The applicant should not have misused the previous loan obtained from the Corporation. The applicant should not have any other similar unit. The applicant should not be a defaulter of the Corporation/banks.
- **Benefits/scope:** Loan for various economic development schemes having unit cost up to ₹50,000/-. Margin Money at 10% of the project cost. Subsidy at 50% of the total project cost, subject to a maximum of ₹10,000/-.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 19

- **Query text:** small business startup funding
- **Original source label (unverified):** Prime Minister Employment Generation Programme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2478
- **Candidate slug:** `pmegp`
- **Scheme name/title:** Prime Minister's Employment Generation Programme
- **Details:** Launched in August 2008, Prime Minister's Employment Generation Programme (PMEGP) is a credit-linked subsidy scheme, administered by the Ministry of Micro, Small and Medium Enterprises (MSME). PMEGP aims to generate employment opportunities through the establishment of micro-enterprises in the non-farm sector for rural as well as urban areas. The scheme has been approved for continuation over the 15th Finance Commission cycle i.e., for the period of five years from 2021-22 to 2025-26. PMEGP was formed by merging the two schemes that were in operation till 31st March 2008, namely Prime Minister's Rojgar Yojana (PMRY) and Rural Employment Generation Programme (REGP). An outlay of ₹13,554.42 Crore has been approved for PMEGP for five Financial Years (2021-22 to 2025-26) to set up about 4,00,000 projects with the creation of 30,00,000 employment @8 persons per unit). In addition, 1,000 Units will be upgraded in each FY. Objectives To generate employment opportunities in rural as well as urban areas of the country through the setting up of new self-employment ventures/projects/micro enterprises. To bring together widely dispersed traditional artisans! rural and urban unemployed youth and give them self-employment opportunities to the extent possible, at their place. To provide continuous and sustainable employment to a large segment of traditional and prospective artisans and rural and urban unemployed youth in the country, so as to help arrest migration of rural youth to urban areas. To increase the wage-earning capacity of workers and artisans and contribute to an increase in the growth rate of rural and urban employment. Implementing Agencies At the National level, the scheme is being implemented by the Khadi and Village Industries Commission (KVIC), a statutory organization under the administrative control of the Ministry of MSME as the single nodal agency. At the State level, the scheme is implemented through State offices of KVIC, State Khadi and Village Industries Boards (KVIBs), District Industries Centre's (DICs), Coir Board (for coir-related activities), and Banks. The government may also involve other suitable agencies for the implementation of the scheme.
- **Eligibility:** For PMEGP new enterprises (Units) Any individual, above 18 years of age. There will be no income ceiling for assistance in setting up projects under PMEGP. For setting up of project costing above Rs.10 lakh in the Manufacturing sector and above ₹ 5,00,000 in the Business /Service sector, the beneficiaries should possess at least VIII standard pass educational qualification. Assistance under the scheme is available only for new projects sanctioned specifically under the PMEGP. Existing Units (under PMRY, REGP, or any other scheme of the Government of India or State Government) and the units that have already availed of Government Subsidy under any other scheme of the Government of India or State Government are not eligible. For up-gradation of existing PMEGP / REGP / MUDRA units Margin Money(subsidy)claimed under PMEGP has to be successfully adjusted on the completion of the lock-in period of 3 years. The first loan under PMEGP/REGP/MUDRA has to be successfully repaid in the stipulated time. The unit is profit-making with good turnover and has the potential for further growth in turnover and profit with modernization/upgrading of the technology. Reservation / Preference / Priority Priority will be given to the persons affected by natural calamities/disasters in the areas which are declared as affected by "disaster" as defined under Section 2(d) of the Disaster Management Act, 2005 by the Ministry of Home Affairs.
- **Benefits/scope:** Funds under PMEGP Scheme will be available under two major heads: 1.  Margin Money Subsidy a) Funds will be allocated under annual Budget Estimates toward disbursement of Margin Money (subsidy) for setting up new micro-enterprises/units; and b) From the funds allocated under BE for the Margin Money subsidy, ₹ 100 Crores or as approved by the competent authority will be earmarked for each FY towards disbursement of Margin Money (subsidy) for the upgradation of existing PMEGP/REGP/MUDRA units. 2.  Backward and Forward Linkages 5% of the total allocation under BE for a Financial Year against PMEGP, or as approved by the competent authority, shall be earmarked as funds under Backward and Forward Linkages and will be utilized for arranging awareness camps, State/District level monitoring meetings, Workshops, Exhibitions, Bankers meetings, TNDA, Publicity, Entrepreneurship Development Programme (EDP) training, Physical verification &amp; Geo-tagging, Evaluation &amp; impacts Assessment study, Setting of Entrepreneurship Facilitation Centre (EFC), Center of Excellence (CoE), Engagement of Field Experts and Data Entry Operators (DEOs), Creation and Upgradation of IT infrastructure, Awards, Call Centre facility, PMU, and other related activities and settlement of other residual liabilities by the KVIC. Levels of support under PMEGP 1.  For setting up new micro-enterprise (units) a) Categories of beneficiaries under PMEGP (for setting up of new enterprises): General Category Beneficiary's contribution (of project cost): 10% Rate of Subsidy (of project cost): 15% for Urban Areas, 25% for Rural Areas. b) Categories of beneficiaries under PMEGP (for setting up of new enterprises): Special Category (including SC, ST, OBC, Minorities, Women, Ex-Servicemen, Transgenders, Differently abled, NER, Aspirational Districts, Hill and Border areas(as notified by the Government), etc. (i) Beneficiary's contribution (of project cost): 05% (ii) Rate of Subsidy (of project cost): 25% for Urban Areas, 35% for Rural Areas. Note: The maximum cost of the project/unit admissible for Margin Money subsidy under the Manufacturing sector is ₹50,00,000. The maximum cost of the project/unit admissible for the Margin Money subsidy under the Business/Service sector is ₹20,00,000. The balance amount (excluding the own contribution)of the total project cost will be provided by Banks. If the total project cost exceeds ₹50,00,000 or ₹20,00,000 for Manufacturing and Service/Business sector respectively, the balance amount may be provided by Banks without any Government subsidy. 2.  2 nd Loan for Upgradation of Existing PMEGP / REGP / MUDRA Units a) Categories of beneficiaries under PMEGP (for upgradation of existing units): All Categories b) Beneficiary's contribution (of project cost): 10% c) Rate of Subsidy (of project cost): 15% (20% in NER and Hill States). Note: 1) The maximum cost of the project/unit admissible for Margin Money subsidy under the Manufacturing sector for upgradation is ₹10,00,00,000. The maximum subsidy would be ₹15,00,000 (₹20,00,000 for NER and Hill States). 2) The maximum cost of the project/unit admissible for Margin Money subsidy under the Business/Service sector for upgradation is ₹25,00,000. The maximum subsidy would be ₹3,75,000 (₹5,00,000 for NER and Hill States). 3) The balance amount (excluding the own contribution)of the total project cost will be provided by Banks. 4) If the total project cost exceeds ₹10,00,00,000 or ₹25,00,000 for Manufacturing and Service/Business sector respectively, the balance amount may be provided by banks without any Government subsidy.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 471
- **Candidate slug:** `cmegp`
- **Scheme name/title:** CHIEF MINISTER  EMPLOYMENT GENERATION  PROGRAMME (CMEGP)
- **Details:** Scheme launched by GR शासन निर्णय क्र. योजना-२०१९/प्र.क्र.१२१/उद्योग ७ dated on 01.08.2019 Scheme will be implemented and monitored by Directorate of Industries (DOI), under the administrative control of Industries Department, Government of Maharashtra. The Scheme will be implemented through District Industries   Canters (DICs), Maharashtra State Khadi and Village Industries Boards (KVIB) under the control of Directorate of Industries and also by banks. ﻿ The maximum cost of the project/unit admissible under manufacturing sector is Rs.50 lakh. The maximum cost of the project/unit admissible under service, Agro-based/ Primary Agro processing sector, E-vehicle based goods transport and other businesses, single brand service ventures (single brand-based chains, mobile service ventures) is Rs.20 lakhs. Beneficiary’s Contribution in the project cost will be 5% to 10 % as per the Categories of Beneficiaries under CMEGP scheme and balance amount of the total project cost will be provided   by Banks as term loan. ﻿
- **Eligibility:** 1)The Age of the applicant should be between 18 to 45. For Special category (including SC/ST/Women/ Ex-servicemen/Differently abled) age is relaxed by 5 years. 2)The Occupation of the applicant should be unemployed youth, Youth willing to establish new ventures. 3)The Annual Income of the Applicant/Family/Parent/Guardian should No criteria LPA 4)The Gender of the applicant should be Male and Female 5)The Marital Status of the applicant should be for all 6)The Educational Qualification of the applicant should be minimum 7th standard pass for   project/unit above Rs. 10 lac and for project/units above Rs.25 lac the required educational criterion for the applicant is minimum 10th standard pass. ﻿
- **Benefits/scope:** ﻿ Categories of beneficiaries under CMEGP Beneficiary’s Contribution (of project cost) Rate of subsidy (of project cost) Area (location of project/unit) ﻿ Urban Rural General Category 10% 15% 25% Special Category (includes SC / ST /Women/ Ex- servicemen / differently abled/VJNT/OBC/Minority) 5% 25% 35% ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1913
- **Candidate slug:** `megp`
- **Scheme name/title:** Migrants Employment Generation Programme
- **Details:** The Government of Tamil Nadu has launched the “Migrants Employment Generation Programme (MEGP)” for the Non-Resident Tamils, who returned back to Tamil Nadu due to Covid-19 Pandemic. This scheme is to be implemented by the Commissionerate of Industries and Commerce and this Commissionerate is the Nodal Agency at the State Level. Also, the Government has ordered that the District Industries Centre (DICs) of the concerned Districts and the Office of the Regional Joint Director of Industries and Commerce in respect of Chennai District is the implementing agencies in coordination with this Commissionerate. The Covid-19 pandemic has wreaked havoc across the global economy. This in turn has rendered many migrants jobless and forced them to return to their own native places. The emigrants who are already skilled in their respective fields as they have been working on that for many years abroad, this scheme will help in tapping the potential of such returnees who want to turn into small scale Entrepreneurs. The scheme will help to mitigate the unemployment problem of the huge number of COVID returnees and will also generate employment for others by converting the eligible one into Small Scale Entrepreneurs. This will be executed after continuous deliberation with the Micro, Small, and Medium Enterprises Departments which have a scheme similar for the unemployed youth of Tamil Nadu. Objectives: To generate employment opportunities for the migrant returnees who have come back to their homeland due to Covid by setting up self-employment ventures in Microenterprises in the Manufacturing service and Business Sectors. To provide livelihood opportunities to the migrant returnees who have lost their jobs and livelihood due to Covid. To facilitate the provision of collateral-free advances under Credit Guarantee Trust for Micro, Small Enterprises (CGTMSE) dovetailing under the Unemployed Youth Employment Generation Programme. Nodal Agency: The Commissionerate of Non-Resident Tamils is the Nodal Agency at the State level and the scheme will be implemented it through the Commissionerate of Industries and Commerce. Areas of operation: The scheme is applicable to all areas in the State including rural and urban areas. Implementing Agencies: District Industries Centre (DICs) of the concerned Districts and the office of the Regional Joint Director of Industries and Commerce in respect of Chennai District will be the implementing agencies in coordination with the Commissionerate of Non-Resident Tamils. Maximum Project cost: ₹15 lakhs for the manufacturing sector, ₹5 lakhs for the service sector and business sector. Promoter’s contribution (Owner’s contribution): 10% for the General category and 5% for the special category (Scheduled Caste / Scheduled Tribes / Backward Classes / Most Backward Classes / Minorities / Women / Physically Challenged / Transgender) Activities covered: All economically viable manufacturing services and business activities excluding direct agricultural operations like raising corporation etc. Training: Training for two days in the “Entrepreneur Development Programme” to be conducted by the Entrepreneur Development Institute (EDI) of the Government of Tamil Nadu is mandatory. However, the training shall be completed within 12 months from the date of selection by the District Task Force Committees (DTFCs). Task Force Committee: The Task Force Committee will comprise of General Manager, District Industries Centre as Chairman, and Personal Assistant (General) to the Collector as representative of the Commissionerate of Rehabilitation. The members of the Committee will be as under: a.	Lead Bank b.	District Manager, Tamil Nadu Adi Dravidar Housing and Collector as Development Corporation Limited (TAHDCO) c.	District Coordinators from Leading Banks in the Districts d.	Representative from District Micro, Small, and Medium Enterprises Associations e. Representative from National Small Industries Corporation Limited/Micro, Small and Medium Enterprises - Development Institute f.	District Employment Officer. Project sanction: The project will be sanctioned by financing branches of the Banks as	per techno-economic viability. Financial Institutions: All Nationalized Banks, Private Sector Banks, and 'Tam Nadu Industrial Co-operative Bank. Collateral: No collateral is required. Amount of the Bank Loan: Banks sanction and release 90-95% loan of the project cost. (Including Government subsidy of 25%) Rate of interest: Normal Bank rate of interest. Repayment period: The repayment Schedule shall be for 5 years after an initial moratorium period of 6 months or the date of commencement of the project whichever is earlier. Defaulter: The applicant should not default in any nationalized bank financial institution / Cooperative bank. Further, a person who has already been assisted under other subsidy-linked Government schemes would not be eligible under this scheme. Marketing Support: As marketing support for the products produced by Migrants Unemployed Youth Employment Generation Program units, Exhibitions, Buyer-Seller Meet, etc., will be arranged by General Manager, District Industries Centres to promote their products and will be done in coordination with the Unemployed Youth Employment Generation Programme (UYEGP). Review &amp; Monitoring: The progress of the Scheme will be reviewed by the District Collector at the Banker's Standing Committee, District Level Co-Ordination Committee (DLCC) / District Level Review Committee (DLRC) meetings conducted periodically with the Bankers. At the State level, the progress of the Scheme will be monitored by the State Level Bankers-Committee (SLBC). The Secretary to Government and Rehabilitation Department will review the progress on a quarterly basis.
- **Eligibility:** The applicant should have returned to Tamil Nadu on &amp; after 01-01-2020 due to the Covid-19 outbreak. The age of the applicant should be between 18 to 45 years in general and for special categories (Women/Minorities/ BC/MBC/SC/ST/Ex-servicemen/Transgender/Differently abled), the age relaxation is up to 55 years. The applicant should possess a minimum educational qualification of 8th standard pass. The family income of the applicant should be below ₹5.00 lakh. The maximum project costs for Manufacturing / Trading / Service projects should be ₹15.00 lakh / ₹5.00 lakh / ₹5.00 lakh respectively. The applicant’s/promoter’s contribution should be 10% of the project cost for the General category and 5% for the Special Category.
- **Benefits/scope:** Under the scheme, the subsidy @ 25% of the project cost will be sanctioned to the beneficiaries subject to a maximum of ₹2.5 lakhs.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 20

- **Query text:** entrepreneurship loan scheme
- **Original source label (unverified):** Prime Minister Employment Generation Programme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2478
- **Candidate slug:** `pmegp`
- **Scheme name/title:** Prime Minister's Employment Generation Programme
- **Details:** Launched in August 2008, Prime Minister's Employment Generation Programme (PMEGP) is a credit-linked subsidy scheme, administered by the Ministry of Micro, Small and Medium Enterprises (MSME). PMEGP aims to generate employment opportunities through the establishment of micro-enterprises in the non-farm sector for rural as well as urban areas. The scheme has been approved for continuation over the 15th Finance Commission cycle i.e., for the period of five years from 2021-22 to 2025-26. PMEGP was formed by merging the two schemes that were in operation till 31st March 2008, namely Prime Minister's Rojgar Yojana (PMRY) and Rural Employment Generation Programme (REGP). An outlay of ₹13,554.42 Crore has been approved for PMEGP for five Financial Years (2021-22 to 2025-26) to set up about 4,00,000 projects with the creation of 30,00,000 employment @8 persons per unit). In addition, 1,000 Units will be upgraded in each FY. Objectives To generate employment opportunities in rural as well as urban areas of the country through the setting up of new self-employment ventures/projects/micro enterprises. To bring together widely dispersed traditional artisans! rural and urban unemployed youth and give them self-employment opportunities to the extent possible, at their place. To provide continuous and sustainable employment to a large segment of traditional and prospective artisans and rural and urban unemployed youth in the country, so as to help arrest migration of rural youth to urban areas. To increase the wage-earning capacity of workers and artisans and contribute to an increase in the growth rate of rural and urban employment. Implementing Agencies At the National level, the scheme is being implemented by the Khadi and Village Industries Commission (KVIC), a statutory organization under the administrative control of the Ministry of MSME as the single nodal agency. At the State level, the scheme is implemented through State offices of KVIC, State Khadi and Village Industries Boards (KVIBs), District Industries Centre's (DICs), Coir Board (for coir-related activities), and Banks. The government may also involve other suitable agencies for the implementation of the scheme.
- **Eligibility:** For PMEGP new enterprises (Units) Any individual, above 18 years of age. There will be no income ceiling for assistance in setting up projects under PMEGP. For setting up of project costing above Rs.10 lakh in the Manufacturing sector and above ₹ 5,00,000 in the Business /Service sector, the beneficiaries should possess at least VIII standard pass educational qualification. Assistance under the scheme is available only for new projects sanctioned specifically under the PMEGP. Existing Units (under PMRY, REGP, or any other scheme of the Government of India or State Government) and the units that have already availed of Government Subsidy under any other scheme of the Government of India or State Government are not eligible. For up-gradation of existing PMEGP / REGP / MUDRA units Margin Money(subsidy)claimed under PMEGP has to be successfully adjusted on the completion of the lock-in period of 3 years. The first loan under PMEGP/REGP/MUDRA has to be successfully repaid in the stipulated time. The unit is profit-making with good turnover and has the potential for further growth in turnover and profit with modernization/upgrading of the technology. Reservation / Preference / Priority Priority will be given to the persons affected by natural calamities/disasters in the areas which are declared as affected by "disaster" as defined under Section 2(d) of the Disaster Management Act, 2005 by the Ministry of Home Affairs.
- **Benefits/scope:** Funds under PMEGP Scheme will be available under two major heads: 1.  Margin Money Subsidy a) Funds will be allocated under annual Budget Estimates toward disbursement of Margin Money (subsidy) for setting up new micro-enterprises/units; and b) From the funds allocated under BE for the Margin Money subsidy, ₹ 100 Crores or as approved by the competent authority will be earmarked for each FY towards disbursement of Margin Money (subsidy) for the upgradation of existing PMEGP/REGP/MUDRA units. 2.  Backward and Forward Linkages 5% of the total allocation under BE for a Financial Year against PMEGP, or as approved by the competent authority, shall be earmarked as funds under Backward and Forward Linkages and will be utilized for arranging awareness camps, State/District level monitoring meetings, Workshops, Exhibitions, Bankers meetings, TNDA, Publicity, Entrepreneurship Development Programme (EDP) training, Physical verification &amp; Geo-tagging, Evaluation &amp; impacts Assessment study, Setting of Entrepreneurship Facilitation Centre (EFC), Center of Excellence (CoE), Engagement of Field Experts and Data Entry Operators (DEOs), Creation and Upgradation of IT infrastructure, Awards, Call Centre facility, PMU, and other related activities and settlement of other residual liabilities by the KVIC. Levels of support under PMEGP 1.  For setting up new micro-enterprise (units) a) Categories of beneficiaries under PMEGP (for setting up of new enterprises): General Category Beneficiary's contribution (of project cost): 10% Rate of Subsidy (of project cost): 15% for Urban Areas, 25% for Rural Areas. b) Categories of beneficiaries under PMEGP (for setting up of new enterprises): Special Category (including SC, ST, OBC, Minorities, Women, Ex-Servicemen, Transgenders, Differently abled, NER, Aspirational Districts, Hill and Border areas(as notified by the Government), etc. (i) Beneficiary's contribution (of project cost): 05% (ii) Rate of Subsidy (of project cost): 25% for Urban Areas, 35% for Rural Areas. Note: The maximum cost of the project/unit admissible for Margin Money subsidy under the Manufacturing sector is ₹50,00,000. The maximum cost of the project/unit admissible for the Margin Money subsidy under the Business/Service sector is ₹20,00,000. The balance amount (excluding the own contribution)of the total project cost will be provided by Banks. If the total project cost exceeds ₹50,00,000 or ₹20,00,000 for Manufacturing and Service/Business sector respectively, the balance amount may be provided by Banks without any Government subsidy. 2.  2 nd Loan for Upgradation of Existing PMEGP / REGP / MUDRA Units a) Categories of beneficiaries under PMEGP (for upgradation of existing units): All Categories b) Beneficiary's contribution (of project cost): 10% c) Rate of Subsidy (of project cost): 15% (20% in NER and Hill States). Note: 1) The maximum cost of the project/unit admissible for Margin Money subsidy under the Manufacturing sector for upgradation is ₹10,00,00,000. The maximum subsidy would be ₹15,00,000 (₹20,00,000 for NER and Hill States). 2) The maximum cost of the project/unit admissible for Margin Money subsidy under the Business/Service sector for upgradation is ₹25,00,000. The maximum subsidy would be ₹3,75,000 (₹5,00,000 for NER and Hill States). 3) The balance amount (excluding the own contribution)of the total project cost will be provided by Banks. 4) If the total project cost exceeds ₹10,00,00,000 or ₹25,00,000 for Manufacturing and Service/Business sector respectively, the balance amount may be provided by banks without any Government subsidy.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 471
- **Candidate slug:** `cmegp`
- **Scheme name/title:** CHIEF MINISTER  EMPLOYMENT GENERATION  PROGRAMME (CMEGP)
- **Details:** Scheme launched by GR शासन निर्णय क्र. योजना-२०१९/प्र.क्र.१२१/उद्योग ७ dated on 01.08.2019 Scheme will be implemented and monitored by Directorate of Industries (DOI), under the administrative control of Industries Department, Government of Maharashtra. The Scheme will be implemented through District Industries   Canters (DICs), Maharashtra State Khadi and Village Industries Boards (KVIB) under the control of Directorate of Industries and also by banks. ﻿ The maximum cost of the project/unit admissible under manufacturing sector is Rs.50 lakh. The maximum cost of the project/unit admissible under service, Agro-based/ Primary Agro processing sector, E-vehicle based goods transport and other businesses, single brand service ventures (single brand-based chains, mobile service ventures) is Rs.20 lakhs. Beneficiary’s Contribution in the project cost will be 5% to 10 % as per the Categories of Beneficiaries under CMEGP scheme and balance amount of the total project cost will be provided   by Banks as term loan. ﻿
- **Eligibility:** 1)The Age of the applicant should be between 18 to 45. For Special category (including SC/ST/Women/ Ex-servicemen/Differently abled) age is relaxed by 5 years. 2)The Occupation of the applicant should be unemployed youth, Youth willing to establish new ventures. 3)The Annual Income of the Applicant/Family/Parent/Guardian should No criteria LPA 4)The Gender of the applicant should be Male and Female 5)The Marital Status of the applicant should be for all 6)The Educational Qualification of the applicant should be minimum 7th standard pass for   project/unit above Rs. 10 lac and for project/units above Rs.25 lac the required educational criterion for the applicant is minimum 10th standard pass. ﻿
- **Benefits/scope:** ﻿ Categories of beneficiaries under CMEGP Beneficiary’s Contribution (of project cost) Rate of subsidy (of project cost) Area (location of project/unit) ﻿ Urban Rural General Category 10% 15% 25% Special Category (includes SC / ST /Women/ Ex- servicemen / differently abled/VJNT/OBC/Minority) 5% 25% 35% ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1913
- **Candidate slug:** `megp`
- **Scheme name/title:** Migrants Employment Generation Programme
- **Details:** The Government of Tamil Nadu has launched the “Migrants Employment Generation Programme (MEGP)” for the Non-Resident Tamils, who returned back to Tamil Nadu due to Covid-19 Pandemic. This scheme is to be implemented by the Commissionerate of Industries and Commerce and this Commissionerate is the Nodal Agency at the State Level. Also, the Government has ordered that the District Industries Centre (DICs) of the concerned Districts and the Office of the Regional Joint Director of Industries and Commerce in respect of Chennai District is the implementing agencies in coordination with this Commissionerate. The Covid-19 pandemic has wreaked havoc across the global economy. This in turn has rendered many migrants jobless and forced them to return to their own native places. The emigrants who are already skilled in their respective fields as they have been working on that for many years abroad, this scheme will help in tapping the potential of such returnees who want to turn into small scale Entrepreneurs. The scheme will help to mitigate the unemployment problem of the huge number of COVID returnees and will also generate employment for others by converting the eligible one into Small Scale Entrepreneurs. This will be executed after continuous deliberation with the Micro, Small, and Medium Enterprises Departments which have a scheme similar for the unemployed youth of Tamil Nadu. Objectives: To generate employment opportunities for the migrant returnees who have come back to their homeland due to Covid by setting up self-employment ventures in Microenterprises in the Manufacturing service and Business Sectors. To provide livelihood opportunities to the migrant returnees who have lost their jobs and livelihood due to Covid. To facilitate the provision of collateral-free advances under Credit Guarantee Trust for Micro, Small Enterprises (CGTMSE) dovetailing under the Unemployed Youth Employment Generation Programme. Nodal Agency: The Commissionerate of Non-Resident Tamils is the Nodal Agency at the State level and the scheme will be implemented it through the Commissionerate of Industries and Commerce. Areas of operation: The scheme is applicable to all areas in the State including rural and urban areas. Implementing Agencies: District Industries Centre (DICs) of the concerned Districts and the office of the Regional Joint Director of Industries and Commerce in respect of Chennai District will be the implementing agencies in coordination with the Commissionerate of Non-Resident Tamils. Maximum Project cost: ₹15 lakhs for the manufacturing sector, ₹5 lakhs for the service sector and business sector. Promoter’s contribution (Owner’s contribution): 10% for the General category and 5% for the special category (Scheduled Caste / Scheduled Tribes / Backward Classes / Most Backward Classes / Minorities / Women / Physically Challenged / Transgender) Activities covered: All economically viable manufacturing services and business activities excluding direct agricultural operations like raising corporation etc. Training: Training for two days in the “Entrepreneur Development Programme” to be conducted by the Entrepreneur Development Institute (EDI) of the Government of Tamil Nadu is mandatory. However, the training shall be completed within 12 months from the date of selection by the District Task Force Committees (DTFCs). Task Force Committee: The Task Force Committee will comprise of General Manager, District Industries Centre as Chairman, and Personal Assistant (General) to the Collector as representative of the Commissionerate of Rehabilitation. The members of the Committee will be as under: a.	Lead Bank b.	District Manager, Tamil Nadu Adi Dravidar Housing and Collector as Development Corporation Limited (TAHDCO) c.	District Coordinators from Leading Banks in the Districts d.	Representative from District Micro, Small, and Medium Enterprises Associations e. Representative from National Small Industries Corporation Limited/Micro, Small and Medium Enterprises - Development Institute f.	District Employment Officer. Project sanction: The project will be sanctioned by financing branches of the Banks as	per techno-economic viability. Financial Institutions: All Nationalized Banks, Private Sector Banks, and 'Tam Nadu Industrial Co-operative Bank. Collateral: No collateral is required. Amount of the Bank Loan: Banks sanction and release 90-95% loan of the project cost. (Including Government subsidy of 25%) Rate of interest: Normal Bank rate of interest. Repayment period: The repayment Schedule shall be for 5 years after an initial moratorium period of 6 months or the date of commencement of the project whichever is earlier. Defaulter: The applicant should not default in any nationalized bank financial institution / Cooperative bank. Further, a person who has already been assisted under other subsidy-linked Government schemes would not be eligible under this scheme. Marketing Support: As marketing support for the products produced by Migrants Unemployed Youth Employment Generation Program units, Exhibitions, Buyer-Seller Meet, etc., will be arranged by General Manager, District Industries Centres to promote their products and will be done in coordination with the Unemployed Youth Employment Generation Programme (UYEGP). Review &amp; Monitoring: The progress of the Scheme will be reviewed by the District Collector at the Banker's Standing Committee, District Level Co-Ordination Committee (DLCC) / District Level Review Committee (DLRC) meetings conducted periodically with the Bankers. At the State level, the progress of the Scheme will be monitored by the State Level Bankers-Committee (SLBC). The Secretary to Government and Rehabilitation Department will review the progress on a quarterly basis.
- **Eligibility:** The applicant should have returned to Tamil Nadu on &amp; after 01-01-2020 due to the Covid-19 outbreak. The age of the applicant should be between 18 to 45 years in general and for special categories (Women/Minorities/ BC/MBC/SC/ST/Ex-servicemen/Transgender/Differently abled), the age relaxation is up to 55 years. The applicant should possess a minimum educational qualification of 8th standard pass. The family income of the applicant should be below ₹5.00 lakh. The maximum project costs for Manufacturing / Trading / Service projects should be ₹15.00 lakh / ₹5.00 lakh / ₹5.00 lakh respectively. The applicant’s/promoter’s contribution should be 10% of the project cost for the General category and 5% for the Special Category.
- **Benefits/scope:** Under the scheme, the subsidy @ 25% of the project cost will be sanctioned to the beneficiaries subject to a maximum of ₹2.5 lakhs.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 21

- **Query text:** self employment assistance
- **Original source label (unverified):** Prime Minister Employment Generation Programme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2478
- **Candidate slug:** `pmegp`
- **Scheme name/title:** Prime Minister's Employment Generation Programme
- **Details:** Launched in August 2008, Prime Minister's Employment Generation Programme (PMEGP) is a credit-linked subsidy scheme, administered by the Ministry of Micro, Small and Medium Enterprises (MSME). PMEGP aims to generate employment opportunities through the establishment of micro-enterprises in the non-farm sector for rural as well as urban areas. The scheme has been approved for continuation over the 15th Finance Commission cycle i.e., for the period of five years from 2021-22 to 2025-26. PMEGP was formed by merging the two schemes that were in operation till 31st March 2008, namely Prime Minister's Rojgar Yojana (PMRY) and Rural Employment Generation Programme (REGP). An outlay of ₹13,554.42 Crore has been approved for PMEGP for five Financial Years (2021-22 to 2025-26) to set up about 4,00,000 projects with the creation of 30,00,000 employment @8 persons per unit). In addition, 1,000 Units will be upgraded in each FY. Objectives To generate employment opportunities in rural as well as urban areas of the country through the setting up of new self-employment ventures/projects/micro enterprises. To bring together widely dispersed traditional artisans! rural and urban unemployed youth and give them self-employment opportunities to the extent possible, at their place. To provide continuous and sustainable employment to a large segment of traditional and prospective artisans and rural and urban unemployed youth in the country, so as to help arrest migration of rural youth to urban areas. To increase the wage-earning capacity of workers and artisans and contribute to an increase in the growth rate of rural and urban employment. Implementing Agencies At the National level, the scheme is being implemented by the Khadi and Village Industries Commission (KVIC), a statutory organization under the administrative control of the Ministry of MSME as the single nodal agency. At the State level, the scheme is implemented through State offices of KVIC, State Khadi and Village Industries Boards (KVIBs), District Industries Centre's (DICs), Coir Board (for coir-related activities), and Banks. The government may also involve other suitable agencies for the implementation of the scheme.
- **Eligibility:** For PMEGP new enterprises (Units) Any individual, above 18 years of age. There will be no income ceiling for assistance in setting up projects under PMEGP. For setting up of project costing above Rs.10 lakh in the Manufacturing sector and above ₹ 5,00,000 in the Business /Service sector, the beneficiaries should possess at least VIII standard pass educational qualification. Assistance under the scheme is available only for new projects sanctioned specifically under the PMEGP. Existing Units (under PMRY, REGP, or any other scheme of the Government of India or State Government) and the units that have already availed of Government Subsidy under any other scheme of the Government of India or State Government are not eligible. For up-gradation of existing PMEGP / REGP / MUDRA units Margin Money(subsidy)claimed under PMEGP has to be successfully adjusted on the completion of the lock-in period of 3 years. The first loan under PMEGP/REGP/MUDRA has to be successfully repaid in the stipulated time. The unit is profit-making with good turnover and has the potential for further growth in turnover and profit with modernization/upgrading of the technology. Reservation / Preference / Priority Priority will be given to the persons affected by natural calamities/disasters in the areas which are declared as affected by "disaster" as defined under Section 2(d) of the Disaster Management Act, 2005 by the Ministry of Home Affairs.
- **Benefits/scope:** Funds under PMEGP Scheme will be available under two major heads: 1.  Margin Money Subsidy a) Funds will be allocated under annual Budget Estimates toward disbursement of Margin Money (subsidy) for setting up new micro-enterprises/units; and b) From the funds allocated under BE for the Margin Money subsidy, ₹ 100 Crores or as approved by the competent authority will be earmarked for each FY towards disbursement of Margin Money (subsidy) for the upgradation of existing PMEGP/REGP/MUDRA units. 2.  Backward and Forward Linkages 5% of the total allocation under BE for a Financial Year against PMEGP, or as approved by the competent authority, shall be earmarked as funds under Backward and Forward Linkages and will be utilized for arranging awareness camps, State/District level monitoring meetings, Workshops, Exhibitions, Bankers meetings, TNDA, Publicity, Entrepreneurship Development Programme (EDP) training, Physical verification &amp; Geo-tagging, Evaluation &amp; impacts Assessment study, Setting of Entrepreneurship Facilitation Centre (EFC), Center of Excellence (CoE), Engagement of Field Experts and Data Entry Operators (DEOs), Creation and Upgradation of IT infrastructure, Awards, Call Centre facility, PMU, and other related activities and settlement of other residual liabilities by the KVIC. Levels of support under PMEGP 1.  For setting up new micro-enterprise (units) a) Categories of beneficiaries under PMEGP (for setting up of new enterprises): General Category Beneficiary's contribution (of project cost): 10% Rate of Subsidy (of project cost): 15% for Urban Areas, 25% for Rural Areas. b) Categories of beneficiaries under PMEGP (for setting up of new enterprises): Special Category (including SC, ST, OBC, Minorities, Women, Ex-Servicemen, Transgenders, Differently abled, NER, Aspirational Districts, Hill and Border areas(as notified by the Government), etc. (i) Beneficiary's contribution (of project cost): 05% (ii) Rate of Subsidy (of project cost): 25% for Urban Areas, 35% for Rural Areas. Note: The maximum cost of the project/unit admissible for Margin Money subsidy under the Manufacturing sector is ₹50,00,000. The maximum cost of the project/unit admissible for the Margin Money subsidy under the Business/Service sector is ₹20,00,000. The balance amount (excluding the own contribution)of the total project cost will be provided by Banks. If the total project cost exceeds ₹50,00,000 or ₹20,00,000 for Manufacturing and Service/Business sector respectively, the balance amount may be provided by Banks without any Government subsidy. 2.  2 nd Loan for Upgradation of Existing PMEGP / REGP / MUDRA Units a) Categories of beneficiaries under PMEGP (for upgradation of existing units): All Categories b) Beneficiary's contribution (of project cost): 10% c) Rate of Subsidy (of project cost): 15% (20% in NER and Hill States). Note: 1) The maximum cost of the project/unit admissible for Margin Money subsidy under the Manufacturing sector for upgradation is ₹10,00,00,000. The maximum subsidy would be ₹15,00,000 (₹20,00,000 for NER and Hill States). 2) The maximum cost of the project/unit admissible for Margin Money subsidy under the Business/Service sector for upgradation is ₹25,00,000. The maximum subsidy would be ₹3,75,000 (₹5,00,000 for NER and Hill States). 3) The balance amount (excluding the own contribution)of the total project cost will be provided by Banks. 4) If the total project cost exceeds ₹10,00,00,000 or ₹25,00,000 for Manufacturing and Service/Business sector respectively, the balance amount may be provided by banks without any Government subsidy.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 471
- **Candidate slug:** `cmegp`
- **Scheme name/title:** CHIEF MINISTER  EMPLOYMENT GENERATION  PROGRAMME (CMEGP)
- **Details:** Scheme launched by GR शासन निर्णय क्र. योजना-२०१९/प्र.क्र.१२१/उद्योग ७ dated on 01.08.2019 Scheme will be implemented and monitored by Directorate of Industries (DOI), under the administrative control of Industries Department, Government of Maharashtra. The Scheme will be implemented through District Industries   Canters (DICs), Maharashtra State Khadi and Village Industries Boards (KVIB) under the control of Directorate of Industries and also by banks. ﻿ The maximum cost of the project/unit admissible under manufacturing sector is Rs.50 lakh. The maximum cost of the project/unit admissible under service, Agro-based/ Primary Agro processing sector, E-vehicle based goods transport and other businesses, single brand service ventures (single brand-based chains, mobile service ventures) is Rs.20 lakhs. Beneficiary’s Contribution in the project cost will be 5% to 10 % as per the Categories of Beneficiaries under CMEGP scheme and balance amount of the total project cost will be provided   by Banks as term loan. ﻿
- **Eligibility:** 1)The Age of the applicant should be between 18 to 45. For Special category (including SC/ST/Women/ Ex-servicemen/Differently abled) age is relaxed by 5 years. 2)The Occupation of the applicant should be unemployed youth, Youth willing to establish new ventures. 3)The Annual Income of the Applicant/Family/Parent/Guardian should No criteria LPA 4)The Gender of the applicant should be Male and Female 5)The Marital Status of the applicant should be for all 6)The Educational Qualification of the applicant should be minimum 7th standard pass for   project/unit above Rs. 10 lac and for project/units above Rs.25 lac the required educational criterion for the applicant is minimum 10th standard pass. ﻿
- **Benefits/scope:** ﻿ Categories of beneficiaries under CMEGP Beneficiary’s Contribution (of project cost) Rate of subsidy (of project cost) Area (location of project/unit) ﻿ Urban Rural General Category 10% 15% 25% Special Category (includes SC / ST /Women/ Ex- servicemen / differently abled/VJNT/OBC/Minority) 5% 25% 35% ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1913
- **Candidate slug:** `megp`
- **Scheme name/title:** Migrants Employment Generation Programme
- **Details:** The Government of Tamil Nadu has launched the “Migrants Employment Generation Programme (MEGP)” for the Non-Resident Tamils, who returned back to Tamil Nadu due to Covid-19 Pandemic. This scheme is to be implemented by the Commissionerate of Industries and Commerce and this Commissionerate is the Nodal Agency at the State Level. Also, the Government has ordered that the District Industries Centre (DICs) of the concerned Districts and the Office of the Regional Joint Director of Industries and Commerce in respect of Chennai District is the implementing agencies in coordination with this Commissionerate. The Covid-19 pandemic has wreaked havoc across the global economy. This in turn has rendered many migrants jobless and forced them to return to their own native places. The emigrants who are already skilled in their respective fields as they have been working on that for many years abroad, this scheme will help in tapping the potential of such returnees who want to turn into small scale Entrepreneurs. The scheme will help to mitigate the unemployment problem of the huge number of COVID returnees and will also generate employment for others by converting the eligible one into Small Scale Entrepreneurs. This will be executed after continuous deliberation with the Micro, Small, and Medium Enterprises Departments which have a scheme similar for the unemployed youth of Tamil Nadu. Objectives: To generate employment opportunities for the migrant returnees who have come back to their homeland due to Covid by setting up self-employment ventures in Microenterprises in the Manufacturing service and Business Sectors. To provide livelihood opportunities to the migrant returnees who have lost their jobs and livelihood due to Covid. To facilitate the provision of collateral-free advances under Credit Guarantee Trust for Micro, Small Enterprises (CGTMSE) dovetailing under the Unemployed Youth Employment Generation Programme. Nodal Agency: The Commissionerate of Non-Resident Tamils is the Nodal Agency at the State level and the scheme will be implemented it through the Commissionerate of Industries and Commerce. Areas of operation: The scheme is applicable to all areas in the State including rural and urban areas. Implementing Agencies: District Industries Centre (DICs) of the concerned Districts and the office of the Regional Joint Director of Industries and Commerce in respect of Chennai District will be the implementing agencies in coordination with the Commissionerate of Non-Resident Tamils. Maximum Project cost: ₹15 lakhs for the manufacturing sector, ₹5 lakhs for the service sector and business sector. Promoter’s contribution (Owner’s contribution): 10% for the General category and 5% for the special category (Scheduled Caste / Scheduled Tribes / Backward Classes / Most Backward Classes / Minorities / Women / Physically Challenged / Transgender) Activities covered: All economically viable manufacturing services and business activities excluding direct agricultural operations like raising corporation etc. Training: Training for two days in the “Entrepreneur Development Programme” to be conducted by the Entrepreneur Development Institute (EDI) of the Government of Tamil Nadu is mandatory. However, the training shall be completed within 12 months from the date of selection by the District Task Force Committees (DTFCs). Task Force Committee: The Task Force Committee will comprise of General Manager, District Industries Centre as Chairman, and Personal Assistant (General) to the Collector as representative of the Commissionerate of Rehabilitation. The members of the Committee will be as under: a.	Lead Bank b.	District Manager, Tamil Nadu Adi Dravidar Housing and Collector as Development Corporation Limited (TAHDCO) c.	District Coordinators from Leading Banks in the Districts d.	Representative from District Micro, Small, and Medium Enterprises Associations e. Representative from National Small Industries Corporation Limited/Micro, Small and Medium Enterprises - Development Institute f.	District Employment Officer. Project sanction: The project will be sanctioned by financing branches of the Banks as	per techno-economic viability. Financial Institutions: All Nationalized Banks, Private Sector Banks, and 'Tam Nadu Industrial Co-operative Bank. Collateral: No collateral is required. Amount of the Bank Loan: Banks sanction and release 90-95% loan of the project cost. (Including Government subsidy of 25%) Rate of interest: Normal Bank rate of interest. Repayment period: The repayment Schedule shall be for 5 years after an initial moratorium period of 6 months or the date of commencement of the project whichever is earlier. Defaulter: The applicant should not default in any nationalized bank financial institution / Cooperative bank. Further, a person who has already been assisted under other subsidy-linked Government schemes would not be eligible under this scheme. Marketing Support: As marketing support for the products produced by Migrants Unemployed Youth Employment Generation Program units, Exhibitions, Buyer-Seller Meet, etc., will be arranged by General Manager, District Industries Centres to promote their products and will be done in coordination with the Unemployed Youth Employment Generation Programme (UYEGP). Review &amp; Monitoring: The progress of the Scheme will be reviewed by the District Collector at the Banker's Standing Committee, District Level Co-Ordination Committee (DLCC) / District Level Review Committee (DLRC) meetings conducted periodically with the Bankers. At the State level, the progress of the Scheme will be monitored by the State Level Bankers-Committee (SLBC). The Secretary to Government and Rehabilitation Department will review the progress on a quarterly basis.
- **Eligibility:** The applicant should have returned to Tamil Nadu on &amp; after 01-01-2020 due to the Covid-19 outbreak. The age of the applicant should be between 18 to 45 years in general and for special categories (Women/Minorities/ BC/MBC/SC/ST/Ex-servicemen/Transgender/Differently abled), the age relaxation is up to 55 years. The applicant should possess a minimum educational qualification of 8th standard pass. The family income of the applicant should be below ₹5.00 lakh. The maximum project costs for Manufacturing / Trading / Service projects should be ₹15.00 lakh / ₹5.00 lakh / ₹5.00 lakh respectively. The applicant’s/promoter’s contribution should be 10% of the project cost for the General category and 5% for the Special Category.
- **Benefits/scope:** Under the scheme, the subsidy @ 25% of the project cost will be sanctioned to the beneficiaries subject to a maximum of ₹2.5 lakhs.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 31

- **Query text:** skill development training programs
- **Original source label (unverified):** Pradhan Mantri Kaushal Vikas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1650
- **Candidate slug:** `kvy`
- **Scheme name/title:** Kaushal Vikas Yojana
- **Details:** This scheme aims to address the skill gap faced by construction workers registered with the Board by providing them with access to essential training opportunities for competency development and technical advancement. Currently, construction workers rely solely on on-the-job experience, lacking formal technical training due to institutional limitations. This hinders their ability to secure fair wages and access better services. Recognizing the financial constraints often preventing workers and their families from pursuing formal training, this scheme offers reimbursement for both training costs and lost wages. By bridging this financial gap, the initiative empowers individuals to elevate their skillsets and career prospects.
- **Eligibility:** Applicant himself or his/her husband/wife/father must be a registered construction worker and his/her contribution must be updated. If the registered worker himself wants to undergo training, then his/her age should be between 18-35. Age dependencies: Dependent wife/ unmarried daughter has no age limit. The maximum age of dependent son is 21 years
- **Benefits/scope:** Training fees and materials: Board will reimburse expenses of institute-fixed fees, textbooks, and other training-related stationery. Exam: After training, will have to pass an assessment test. Wages : In case the registered worker himself receives training, an amount equivalent to the minimum wage of the unskilled worker will be reimbursed but only registered workers are eligible, not dependents.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2432
- **Candidate slug:** `pmsby`
- **Scheme name/title:** Pradhan Mantri Suraksha Bima Yojana
- **Details:** An Accident Insurance Scheme offering accidental death and disability cover for death or disability on account of an accident. Premium: Rs.20/- per annum per member. The premium will be deducted from the account holder’s bank / Post office account through ‘auto debit’ facility on or before 1st June of each annual coverage period under the scheme. Coverage Duration: Coverage under PMJJBY is valid for one year from 1st June to 31st May on payment of annual premium. Accident cover assurance termination: The accident cover of the member shall terminate / be restricted accordingly on any of the following events: •	On attaining age 70 years (age nearer birth day). •	Closure of account with the Bank or insufficiency of balance to keep the insurance in force. In case a member is covered under PMSBY through more than one account and premium is received by insurance company inadvertently, insurance cover will be restricted to Rs. 2 lakh.
- **Eligibility:** Individual bank account holders of participating banks aged between 18 years (completed) and 70 years (age nearer birthday) who give their consent to join / enable auto-debit, will be enrolled into the scheme.
- **Benefits/scope:** On Death- the Nominee shall get Rs. 2 Lakhs. Total and irrecoverable loss of both eyes or loss of use of both hands or feet or loss of sight of one eye and loss of use of hand or foot-  Subscriber shall get Rs. 2 Lakhs. Total and irrecoverable loss of sight of one eye or loss of use of one hand or foot –subscriber shall get Rs. 1 Lakh.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 32

- **Query text:** vocational training scheme
- **Original source label (unverified):** Pradhan Mantri Kaushal Vikas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1650
- **Candidate slug:** `kvy`
- **Scheme name/title:** Kaushal Vikas Yojana
- **Details:** This scheme aims to address the skill gap faced by construction workers registered with the Board by providing them with access to essential training opportunities for competency development and technical advancement. Currently, construction workers rely solely on on-the-job experience, lacking formal technical training due to institutional limitations. This hinders their ability to secure fair wages and access better services. Recognizing the financial constraints often preventing workers and their families from pursuing formal training, this scheme offers reimbursement for both training costs and lost wages. By bridging this financial gap, the initiative empowers individuals to elevate their skillsets and career prospects.
- **Eligibility:** Applicant himself or his/her husband/wife/father must be a registered construction worker and his/her contribution must be updated. If the registered worker himself wants to undergo training, then his/her age should be between 18-35. Age dependencies: Dependent wife/ unmarried daughter has no age limit. The maximum age of dependent son is 21 years
- **Benefits/scope:** Training fees and materials: Board will reimburse expenses of institute-fixed fees, textbooks, and other training-related stationery. Exam: After training, will have to pass an assessment test. Wages : In case the registered worker himself receives training, an amount equivalent to the minimum wage of the unskilled worker will be reimbursed but only registered workers are eligible, not dependents.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2432
- **Candidate slug:** `pmsby`
- **Scheme name/title:** Pradhan Mantri Suraksha Bima Yojana
- **Details:** An Accident Insurance Scheme offering accidental death and disability cover for death or disability on account of an accident. Premium: Rs.20/- per annum per member. The premium will be deducted from the account holder’s bank / Post office account through ‘auto debit’ facility on or before 1st June of each annual coverage period under the scheme. Coverage Duration: Coverage under PMJJBY is valid for one year from 1st June to 31st May on payment of annual premium. Accident cover assurance termination: The accident cover of the member shall terminate / be restricted accordingly on any of the following events: •	On attaining age 70 years (age nearer birth day). •	Closure of account with the Bank or insufficiency of balance to keep the insurance in force. In case a member is covered under PMSBY through more than one account and premium is received by insurance company inadvertently, insurance cover will be restricted to Rs. 2 lakh.
- **Eligibility:** Individual bank account holders of participating banks aged between 18 years (completed) and 70 years (age nearer birthday) who give their consent to join / enable auto-debit, will be enrolled into the scheme.
- **Benefits/scope:** On Death- the Nominee shall get Rs. 2 Lakhs. Total and irrecoverable loss of both eyes or loss of use of both hands or feet or loss of sight of one eye and loss of use of hand or foot-  Subscriber shall get Rs. 2 Lakhs. Total and irrecoverable loss of sight of one eye or loss of use of one hand or foot –subscriber shall get Rs. 1 Lakh.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 33

- **Query text:** job training government initiative
- **Original source label (unverified):** Pradhan Mantri Kaushal Vikas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1650
- **Candidate slug:** `kvy`
- **Scheme name/title:** Kaushal Vikas Yojana
- **Details:** This scheme aims to address the skill gap faced by construction workers registered with the Board by providing them with access to essential training opportunities for competency development and technical advancement. Currently, construction workers rely solely on on-the-job experience, lacking formal technical training due to institutional limitations. This hinders their ability to secure fair wages and access better services. Recognizing the financial constraints often preventing workers and their families from pursuing formal training, this scheme offers reimbursement for both training costs and lost wages. By bridging this financial gap, the initiative empowers individuals to elevate their skillsets and career prospects.
- **Eligibility:** Applicant himself or his/her husband/wife/father must be a registered construction worker and his/her contribution must be updated. If the registered worker himself wants to undergo training, then his/her age should be between 18-35. Age dependencies: Dependent wife/ unmarried daughter has no age limit. The maximum age of dependent son is 21 years
- **Benefits/scope:** Training fees and materials: Board will reimburse expenses of institute-fixed fees, textbooks, and other training-related stationery. Exam: After training, will have to pass an assessment test. Wages : In case the registered worker himself receives training, an amount equivalent to the minimum wage of the unskilled worker will be reimbursed but only registered workers are eligible, not dependents.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2432
- **Candidate slug:** `pmsby`
- **Scheme name/title:** Pradhan Mantri Suraksha Bima Yojana
- **Details:** An Accident Insurance Scheme offering accidental death and disability cover for death or disability on account of an accident. Premium: Rs.20/- per annum per member. The premium will be deducted from the account holder’s bank / Post office account through ‘auto debit’ facility on or before 1st June of each annual coverage period under the scheme. Coverage Duration: Coverage under PMJJBY is valid for one year from 1st June to 31st May on payment of annual premium. Accident cover assurance termination: The accident cover of the member shall terminate / be restricted accordingly on any of the following events: •	On attaining age 70 years (age nearer birth day). •	Closure of account with the Bank or insufficiency of balance to keep the insurance in force. In case a member is covered under PMSBY through more than one account and premium is received by insurance company inadvertently, insurance cover will be restricted to Rs. 2 lakh.
- **Eligibility:** Individual bank account holders of participating banks aged between 18 years (completed) and 70 years (age nearer birthday) who give their consent to join / enable auto-debit, will be enrolled into the scheme.
- **Benefits/scope:** On Death- the Nominee shall get Rs. 2 Lakhs. Total and irrecoverable loss of both eyes or loss of use of both hands or feet or loss of sight of one eye and loss of use of hand or foot-  Subscriber shall get Rs. 2 Lakhs. Total and irrecoverable loss of sight of one eye or loss of use of one hand or foot –subscriber shall get Rs. 1 Lakh.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 34

- **Query text:** labor welfare benefits schemes
- **Original source label (unverified):** Building and Construction Workers Welfare Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 537
- **Candidate slug:** `cmbocwhrs`
- **Scheme name/title:** Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme
- **Details:** Launched in 2013, the scheme "Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme" aims to provide permanent houses to registered construction workers in the rural areas of Madhya Pradesh who are homeless or living in kutcha/semi-pucca houses. This scheme is applicable in all rural areas of the state (excluding urban and Nazul outer areas).
- **Eligibility:** For Registration: The applicant should be a resident of Madhya Pradesh. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in any building or other construction work for at least 90 days during the preceding 12 months. The registration of the applicant should be renewed annually. For Application: The applicant should not fulfil the eligibility criteria for housing grants under Indira Awas Yojana or Chief Minister Antyodaya Awas Yojana. The applicant should have a family with a maximum of three hectares of agricultural land. The applicant's family's maximum income from all sources should be up to ₹3 lakh per annum. The applicant should have sufficient land available for house construction, as mentioned in clause 6 above. The applicant should be eligible to receive land for housing from the government. The applicant should be willing to construct a house on agricultural land owned by them. The applicant should be eligible to obtain a landholder certificate in the village population. The applicant should agree to obtain a bank loan for constructing a house with a 225 sq. ft. plinth area in the prescribed layout and provide their own contribution in the form of labour/material/inclusion.
- **Benefits/scope:** The Board reimburses a minimum loan grant of ₹50,000 to the beneficiary. The Banks may approve an additional loan of up to ₹30,000 based on repayment capacity, with no role for the State Government. The grant is limited to ₹50,000 per case. NOTE:  The Board provides the grant to District Labour Offices, which distribute it to banks based on approved loan cases.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2564
- **Candidate slug:** `rpcs`
- **Scheme name/title:** Rearing Pond Construction Scheme
- **Details:** The "Rearing Tank Construction Scheme" by the Department of Agriculture, Animal Husbandry, and Cooperation (Fisheries Division), Government of Jharkhand, aims to support private-sector fish farming by constructing rearing tanks for sustainable fish production. Under this scheme, financial assistance is provided to beneficiaries for the construction of rearing ponds with a minimum water area of one acre.
- **Eligibility:** The applicant should be a fisherman. The applicant whose proposed land is near their residence, consisting of one, two, or three plots of "don" land. The applicant should be engaged in fish farming or have constructed a fish seed hatchery with a departmental subsidy. The land proposed for pond construction must be undisputed.  At least 130 decimals of land are required for a 100 decimal water area. For larger ponds, the ratio of water area to total land should be at least 1:1.3. The proposed land must not be mortgaged against any bank loan. The applicant must have valid possession of the proposed land and provide the necessary documentation. The applicant should be financially capable of contributing their share of the pond construction costs.
- **Benefits/scope:** Financial Assistance: SC/ST beneficiaries receive up to 80% of the total cost (maximum ₹4,00,000/-). Other categories receive up to 70% (maximum ₹3,50,000/-). Pond Construction Support: Assistance for constructing one-acre rearing ponds using machinery. Mode of Disbursement: Direct Benefit Transfer (DBT) to beneficiaries' bank accounts. Installments: First installment: ₹1,00,000 after one to two feet of excavation. Second installment: ₹2,00,000 after three feet of excavation. Remaining funds after full excavation and dressing verification.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 463
- **Candidate slug:** `bocs`
- **Scheme name/title:** Building And Other Construction Scholarship
- **Details:** Detailed Students who are pursuing technical or engineering education can apply online under the BOC Scholarship for getting the scholarship amounts. The student must belong to the SC category. Students must be pursuing his or her technical education at a recognized university. ﻿ The main objective of launching the BOC Scholarship is to provide scholarships to students pursuing technical education who have secured good or excellent merit records while carrying out their studies. This will provide social security provisions to the student belonging to the SC category or community. The student must be an ITI/ITC Polytechnic or Diploma. ﻿ Another objective of launching the BOC Scholarship is to provide social and economic welfare to the students so that they will be able to carry out their technical studies while getting the scholarship amount. The Department of Skill Development &amp; Technical Education will initiate all scholarship operations. ﻿
- **Eligibility:** The applicants will need to follow the mentioned eligibility criteria for getting online registration under this scholarship: – The student must be a permanent resident of Odisha. The student must belong to the SC category. The applicant must be pursuing technical education or ITI/Polytechnic courses. ﻿
- **Benefits/scope:** Benefits This scholarship offers various opportunities to SC-category students across the world. Under this scheme, the selected students will receive variable financial support from the Odisha government. Under the BOC scholarship, no living costs of the students are covered. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 35

- **Query text:** worker protection government
- **Original source label (unverified):** Building and Construction Workers Welfare Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 537
- **Candidate slug:** `cmbocwhrs`
- **Scheme name/title:** Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme
- **Details:** Launched in 2013, the scheme "Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme" aims to provide permanent houses to registered construction workers in the rural areas of Madhya Pradesh who are homeless or living in kutcha/semi-pucca houses. This scheme is applicable in all rural areas of the state (excluding urban and Nazul outer areas).
- **Eligibility:** For Registration: The applicant should be a resident of Madhya Pradesh. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in any building or other construction work for at least 90 days during the preceding 12 months. The registration of the applicant should be renewed annually. For Application: The applicant should not fulfil the eligibility criteria for housing grants under Indira Awas Yojana or Chief Minister Antyodaya Awas Yojana. The applicant should have a family with a maximum of three hectares of agricultural land. The applicant's family's maximum income from all sources should be up to ₹3 lakh per annum. The applicant should have sufficient land available for house construction, as mentioned in clause 6 above. The applicant should be eligible to receive land for housing from the government. The applicant should be willing to construct a house on agricultural land owned by them. The applicant should be eligible to obtain a landholder certificate in the village population. The applicant should agree to obtain a bank loan for constructing a house with a 225 sq. ft. plinth area in the prescribed layout and provide their own contribution in the form of labour/material/inclusion.
- **Benefits/scope:** The Board reimburses a minimum loan grant of ₹50,000 to the beneficiary. The Banks may approve an additional loan of up to ₹30,000 based on repayment capacity, with no role for the State Government. The grant is limited to ₹50,000 per case. NOTE:  The Board provides the grant to District Labour Offices, which distribute it to banks based on approved loan cases.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2564
- **Candidate slug:** `rpcs`
- **Scheme name/title:** Rearing Pond Construction Scheme
- **Details:** The "Rearing Tank Construction Scheme" by the Department of Agriculture, Animal Husbandry, and Cooperation (Fisheries Division), Government of Jharkhand, aims to support private-sector fish farming by constructing rearing tanks for sustainable fish production. Under this scheme, financial assistance is provided to beneficiaries for the construction of rearing ponds with a minimum water area of one acre.
- **Eligibility:** The applicant should be a fisherman. The applicant whose proposed land is near their residence, consisting of one, two, or three plots of "don" land. The applicant should be engaged in fish farming or have constructed a fish seed hatchery with a departmental subsidy. The land proposed for pond construction must be undisputed.  At least 130 decimals of land are required for a 100 decimal water area. For larger ponds, the ratio of water area to total land should be at least 1:1.3. The proposed land must not be mortgaged against any bank loan. The applicant must have valid possession of the proposed land and provide the necessary documentation. The applicant should be financially capable of contributing their share of the pond construction costs.
- **Benefits/scope:** Financial Assistance: SC/ST beneficiaries receive up to 80% of the total cost (maximum ₹4,00,000/-). Other categories receive up to 70% (maximum ₹3,50,000/-). Pond Construction Support: Assistance for constructing one-acre rearing ponds using machinery. Mode of Disbursement: Direct Benefit Transfer (DBT) to beneficiaries' bank accounts. Installments: First installment: ₹1,00,000 after one to two feet of excavation. Second installment: ₹2,00,000 after three feet of excavation. Remaining funds after full excavation and dressing verification.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 463
- **Candidate slug:** `bocs`
- **Scheme name/title:** Building And Other Construction Scholarship
- **Details:** Detailed Students who are pursuing technical or engineering education can apply online under the BOC Scholarship for getting the scholarship amounts. The student must belong to the SC category. Students must be pursuing his or her technical education at a recognized university. ﻿ The main objective of launching the BOC Scholarship is to provide scholarships to students pursuing technical education who have secured good or excellent merit records while carrying out their studies. This will provide social security provisions to the student belonging to the SC category or community. The student must be an ITI/ITC Polytechnic or Diploma. ﻿ Another objective of launching the BOC Scholarship is to provide social and economic welfare to the students so that they will be able to carry out their technical studies while getting the scholarship amount. The Department of Skill Development &amp; Technical Education will initiate all scholarship operations. ﻿
- **Eligibility:** The applicants will need to follow the mentioned eligibility criteria for getting online registration under this scholarship: – The student must be a permanent resident of Odisha. The student must belong to the SC category. The applicant must be pursuing technical education or ITI/Polytechnic courses. ﻿
- **Benefits/scope:** Benefits This scholarship offers various opportunities to SC-category students across the world. Under this scheme, the selected students will receive variable financial support from the Odisha government. Under the BOC scholarship, no living costs of the students are covered. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 36

- **Query text:** occupational safety assistance
- **Original source label (unverified):** Building and Construction Workers Welfare Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 537
- **Candidate slug:** `cmbocwhrs`
- **Scheme name/title:** Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme
- **Details:** Launched in 2013, the scheme "Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme" aims to provide permanent houses to registered construction workers in the rural areas of Madhya Pradesh who are homeless or living in kutcha/semi-pucca houses. This scheme is applicable in all rural areas of the state (excluding urban and Nazul outer areas).
- **Eligibility:** For Registration: The applicant should be a resident of Madhya Pradesh. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in any building or other construction work for at least 90 days during the preceding 12 months. The registration of the applicant should be renewed annually. For Application: The applicant should not fulfil the eligibility criteria for housing grants under Indira Awas Yojana or Chief Minister Antyodaya Awas Yojana. The applicant should have a family with a maximum of three hectares of agricultural land. The applicant's family's maximum income from all sources should be up to ₹3 lakh per annum. The applicant should have sufficient land available for house construction, as mentioned in clause 6 above. The applicant should be eligible to receive land for housing from the government. The applicant should be willing to construct a house on agricultural land owned by them. The applicant should be eligible to obtain a landholder certificate in the village population. The applicant should agree to obtain a bank loan for constructing a house with a 225 sq. ft. plinth area in the prescribed layout and provide their own contribution in the form of labour/material/inclusion.
- **Benefits/scope:** The Board reimburses a minimum loan grant of ₹50,000 to the beneficiary. The Banks may approve an additional loan of up to ₹30,000 based on repayment capacity, with no role for the State Government. The grant is limited to ₹50,000 per case. NOTE:  The Board provides the grant to District Labour Offices, which distribute it to banks based on approved loan cases.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2564
- **Candidate slug:** `rpcs`
- **Scheme name/title:** Rearing Pond Construction Scheme
- **Details:** The "Rearing Tank Construction Scheme" by the Department of Agriculture, Animal Husbandry, and Cooperation (Fisheries Division), Government of Jharkhand, aims to support private-sector fish farming by constructing rearing tanks for sustainable fish production. Under this scheme, financial assistance is provided to beneficiaries for the construction of rearing ponds with a minimum water area of one acre.
- **Eligibility:** The applicant should be a fisherman. The applicant whose proposed land is near their residence, consisting of one, two, or three plots of "don" land. The applicant should be engaged in fish farming or have constructed a fish seed hatchery with a departmental subsidy. The land proposed for pond construction must be undisputed.  At least 130 decimals of land are required for a 100 decimal water area. For larger ponds, the ratio of water area to total land should be at least 1:1.3. The proposed land must not be mortgaged against any bank loan. The applicant must have valid possession of the proposed land and provide the necessary documentation. The applicant should be financially capable of contributing their share of the pond construction costs.
- **Benefits/scope:** Financial Assistance: SC/ST beneficiaries receive up to 80% of the total cost (maximum ₹4,00,000/-). Other categories receive up to 70% (maximum ₹3,50,000/-). Pond Construction Support: Assistance for constructing one-acre rearing ponds using machinery. Mode of Disbursement: Direct Benefit Transfer (DBT) to beneficiaries' bank accounts. Installments: First installment: ₹1,00,000 after one to two feet of excavation. Second installment: ₹2,00,000 after three feet of excavation. Remaining funds after full excavation and dressing verification.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 463
- **Candidate slug:** `bocs`
- **Scheme name/title:** Building And Other Construction Scholarship
- **Details:** Detailed Students who are pursuing technical or engineering education can apply online under the BOC Scholarship for getting the scholarship amounts. The student must belong to the SC category. Students must be pursuing his or her technical education at a recognized university. ﻿ The main objective of launching the BOC Scholarship is to provide scholarships to students pursuing technical education who have secured good or excellent merit records while carrying out their studies. This will provide social security provisions to the student belonging to the SC category or community. The student must be an ITI/ITC Polytechnic or Diploma. ﻿ Another objective of launching the BOC Scholarship is to provide social and economic welfare to the students so that they will be able to carry out their technical studies while getting the scholarship amount. The Department of Skill Development &amp; Technical Education will initiate all scholarship operations. ﻿
- **Eligibility:** The applicants will need to follow the mentioned eligibility criteria for getting online registration under this scholarship: – The student must be a permanent resident of Odisha. The student must belong to the SC category. The applicant must be pursuing technical education or ITI/Polytechnic courses. ﻿
- **Benefits/scope:** Benefits This scholarship offers various opportunities to SC-category students across the world. Under this scheme, the selected students will receive variable financial support from the Odisha government. Under the BOC scholarship, no living costs of the students are covered. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 40

- **Query text:** maternity benefit scheme
- **Original source label (unverified):** Pradhan Mantri Maternity Benefit Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1842
- **Candidate slug:** `mbwb`
- **Scheme name/title:** Maternity Benefit
- **Details:** The "Maternity Benefit'' scheme by the Building and Other Construction Workers Welfare Board, Labour Department, West Bengal, is a welfare scheme for the registered workers of the board. Under this scheme, the Board shall provide financial benefit during the period of maternity to the female beneficiary or wife in case of a male beneficiary who is registered for 1 year under the Board, subject to a maximum 2 times in his/ her whole life time.
- **Eligibility:** For Registration as a Building/ Construction Worker: The applicant should be a resident of West Bengal. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in building and construction work for at least 90 days in a given year. For the Application of the Welfare Scheme: The applicant should be a registered female member or wife of a male member Under the Building and Other Construction Workers Welfare Board of West Bengal. The applicant should be pregnant.
- **Benefits/scope:** Quantum of Assistance: ₹6,000/-. Note: The benefit shall be allowed for two times in beneficiarie's whole life time. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1843
- **Candidate slug:** `mbabocwwb`
- **Scheme name/title:** Maternity Benefit (A.B.O.C.W.W.B)
- **Details:** The scheme “Maternity Benefit” was started by the Assam Building and Other Construction Workers Welfare Board (A.B.O.C.W.W.B), Labour Welfare Department, Government of Assam. Under this scheme, financial assistance shall be given to the registered women beneficiaries as maternity benefits during the period of maternity. This benefit shall be allowed twice only.
- **Eligibility:** The applicant should be a permanent resident of Assam. The applicant should be a woman worker. The applicant should be engaged in any building &amp; other construction work. The construction worker should be registered with the Assam Building and Other Construction Workers Welfare Board. The applicant should have an active membership with the Board. The benefit under this scheme shall be given for the birth of two children only.
- **Benefits/scope:** The registered woman beneficiary shall be given ₹20,000/- each as maternity benefit during the period of maternity.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1848
- **Candidate slug:** `mbobocwwb`
- **Scheme name/title:** Maternity Benefit (O.B.O.C.W.W.B)
- **Details:** The “Maternity Benefit” scheme by the Building and Other Construction Workers Welfare Board, Labour Department, Odisha, is a welfare scheme for the registered workers of the board. Under this scheme, the Board shall provide financial assistance in the form of maternity benefits to the female beneficiaries subject to a maximum of two children who  are registered beneficiaries for a period of more than one year under the Odisha Building and Other Construction Workers Welfare Board. ﻿
- **Eligibility:** For Registration as a Building/ Construction Worker: The applicant should be a resident of Odisha. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in building and construction work for at least 90 days in a given year. The applicant should not be a member of any other Welfare Fund established under any law. For the Application of the Welfare Scheme: The applicant should be female. The applicant should be a registered member of the Odisha Building and Other Construction Workers Welfare Board. The applicant should be registered for a period of one year or more under the board. The applicant should be pregnant.
- **Benefits/scope:** Quantum of Assistance: ₹8,000/- to ₹10,000/- per Child. For eligible beneficiaries under “Mamata” being implemented by W&amp;CD Department: ₹15,000/- (₹10,000/- under OB&amp;OCWW Board and ₹5,000/- under “Mamata”). Note: Assistance shall be given for a maximum of two children. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 41

- **Query text:** pregnant women financial assistance
- **Original source label (unverified):** Pradhan Mantri Maternity Benefit Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1842
- **Candidate slug:** `mbwb`
- **Scheme name/title:** Maternity Benefit
- **Details:** The "Maternity Benefit'' scheme by the Building and Other Construction Workers Welfare Board, Labour Department, West Bengal, is a welfare scheme for the registered workers of the board. Under this scheme, the Board shall provide financial benefit during the period of maternity to the female beneficiary or wife in case of a male beneficiary who is registered for 1 year under the Board, subject to a maximum 2 times in his/ her whole life time.
- **Eligibility:** For Registration as a Building/ Construction Worker: The applicant should be a resident of West Bengal. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in building and construction work for at least 90 days in a given year. For the Application of the Welfare Scheme: The applicant should be a registered female member or wife of a male member Under the Building and Other Construction Workers Welfare Board of West Bengal. The applicant should be pregnant.
- **Benefits/scope:** Quantum of Assistance: ₹6,000/-. Note: The benefit shall be allowed for two times in beneficiarie's whole life time. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1843
- **Candidate slug:** `mbabocwwb`
- **Scheme name/title:** Maternity Benefit (A.B.O.C.W.W.B)
- **Details:** The scheme “Maternity Benefit” was started by the Assam Building and Other Construction Workers Welfare Board (A.B.O.C.W.W.B), Labour Welfare Department, Government of Assam. Under this scheme, financial assistance shall be given to the registered women beneficiaries as maternity benefits during the period of maternity. This benefit shall be allowed twice only.
- **Eligibility:** The applicant should be a permanent resident of Assam. The applicant should be a woman worker. The applicant should be engaged in any building &amp; other construction work. The construction worker should be registered with the Assam Building and Other Construction Workers Welfare Board. The applicant should have an active membership with the Board. The benefit under this scheme shall be given for the birth of two children only.
- **Benefits/scope:** The registered woman beneficiary shall be given ₹20,000/- each as maternity benefit during the period of maternity.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1848
- **Candidate slug:** `mbobocwwb`
- **Scheme name/title:** Maternity Benefit (O.B.O.C.W.W.B)
- **Details:** The “Maternity Benefit” scheme by the Building and Other Construction Workers Welfare Board, Labour Department, Odisha, is a welfare scheme for the registered workers of the board. Under this scheme, the Board shall provide financial assistance in the form of maternity benefits to the female beneficiaries subject to a maximum of two children who  are registered beneficiaries for a period of more than one year under the Odisha Building and Other Construction Workers Welfare Board. ﻿
- **Eligibility:** For Registration as a Building/ Construction Worker: The applicant should be a resident of Odisha. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in building and construction work for at least 90 days in a given year. The applicant should not be a member of any other Welfare Fund established under any law. For the Application of the Welfare Scheme: The applicant should be female. The applicant should be a registered member of the Odisha Building and Other Construction Workers Welfare Board. The applicant should be registered for a period of one year or more under the board. The applicant should be pregnant.
- **Benefits/scope:** Quantum of Assistance: ₹8,000/- to ₹10,000/- per Child. For eligible beneficiaries under “Mamata” being implemented by W&amp;CD Department: ₹15,000/- (₹10,000/- under OB&amp;OCWW Board and ₹5,000/- under “Mamata”). Note: Assistance shall be given for a maximum of two children. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 42

- **Query text:** mother and child support
- **Original source label (unverified):** Pradhan Mantri Maternity Benefit Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1842
- **Candidate slug:** `mbwb`
- **Scheme name/title:** Maternity Benefit
- **Details:** The "Maternity Benefit'' scheme by the Building and Other Construction Workers Welfare Board, Labour Department, West Bengal, is a welfare scheme for the registered workers of the board. Under this scheme, the Board shall provide financial benefit during the period of maternity to the female beneficiary or wife in case of a male beneficiary who is registered for 1 year under the Board, subject to a maximum 2 times in his/ her whole life time.
- **Eligibility:** For Registration as a Building/ Construction Worker: The applicant should be a resident of West Bengal. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in building and construction work for at least 90 days in a given year. For the Application of the Welfare Scheme: The applicant should be a registered female member or wife of a male member Under the Building and Other Construction Workers Welfare Board of West Bengal. The applicant should be pregnant.
- **Benefits/scope:** Quantum of Assistance: ₹6,000/-. Note: The benefit shall be allowed for two times in beneficiarie's whole life time. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1843
- **Candidate slug:** `mbabocwwb`
- **Scheme name/title:** Maternity Benefit (A.B.O.C.W.W.B)
- **Details:** The scheme “Maternity Benefit” was started by the Assam Building and Other Construction Workers Welfare Board (A.B.O.C.W.W.B), Labour Welfare Department, Government of Assam. Under this scheme, financial assistance shall be given to the registered women beneficiaries as maternity benefits during the period of maternity. This benefit shall be allowed twice only.
- **Eligibility:** The applicant should be a permanent resident of Assam. The applicant should be a woman worker. The applicant should be engaged in any building &amp; other construction work. The construction worker should be registered with the Assam Building and Other Construction Workers Welfare Board. The applicant should have an active membership with the Board. The benefit under this scheme shall be given for the birth of two children only.
- **Benefits/scope:** The registered woman beneficiary shall be given ₹20,000/- each as maternity benefit during the period of maternity.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 1848
- **Candidate slug:** `mbobocwwb`
- **Scheme name/title:** Maternity Benefit (O.B.O.C.W.W.B)
- **Details:** The “Maternity Benefit” scheme by the Building and Other Construction Workers Welfare Board, Labour Department, Odisha, is a welfare scheme for the registered workers of the board. Under this scheme, the Board shall provide financial assistance in the form of maternity benefits to the female beneficiaries subject to a maximum of two children who  are registered beneficiaries for a period of more than one year under the Odisha Building and Other Construction Workers Welfare Board. ﻿
- **Eligibility:** For Registration as a Building/ Construction Worker: The applicant should be a resident of Odisha. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in building and construction work for at least 90 days in a given year. The applicant should not be a member of any other Welfare Fund established under any law. For the Application of the Welfare Scheme: The applicant should be female. The applicant should be a registered member of the Odisha Building and Other Construction Workers Welfare Board. The applicant should be registered for a period of one year or more under the board. The applicant should be pregnant.
- **Benefits/scope:** Quantum of Assistance: ₹8,000/- to ₹10,000/- per Child. For eligible beneficiaries under “Mamata” being implemented by W&amp;CD Department: ₹15,000/- (₹10,000/- under OB&amp;OCWW Board and ₹5,000/- under “Mamata”). Note: Assistance shall be given for a maximum of two children. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 43

- **Query text:** social security for workers
- **Original source label (unverified):** Building and Construction Workers Welfare Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 537
- **Candidate slug:** `cmbocwhrs`
- **Scheme name/title:** Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme
- **Details:** Launched in 2013, the scheme "Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme" aims to provide permanent houses to registered construction workers in the rural areas of Madhya Pradesh who are homeless or living in kutcha/semi-pucca houses. This scheme is applicable in all rural areas of the state (excluding urban and Nazul outer areas).
- **Eligibility:** For Registration: The applicant should be a resident of Madhya Pradesh. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in any building or other construction work for at least 90 days during the preceding 12 months. The registration of the applicant should be renewed annually. For Application: The applicant should not fulfil the eligibility criteria for housing grants under Indira Awas Yojana or Chief Minister Antyodaya Awas Yojana. The applicant should have a family with a maximum of three hectares of agricultural land. The applicant's family's maximum income from all sources should be up to ₹3 lakh per annum. The applicant should have sufficient land available for house construction, as mentioned in clause 6 above. The applicant should be eligible to receive land for housing from the government. The applicant should be willing to construct a house on agricultural land owned by them. The applicant should be eligible to obtain a landholder certificate in the village population. The applicant should agree to obtain a bank loan for constructing a house with a 225 sq. ft. plinth area in the prescribed layout and provide their own contribution in the form of labour/material/inclusion.
- **Benefits/scope:** The Board reimburses a minimum loan grant of ₹50,000 to the beneficiary. The Banks may approve an additional loan of up to ₹30,000 based on repayment capacity, with no role for the State Government. The grant is limited to ₹50,000 per case. NOTE:  The Board provides the grant to District Labour Offices, which distribute it to banks based on approved loan cases.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2564
- **Candidate slug:** `rpcs`
- **Scheme name/title:** Rearing Pond Construction Scheme
- **Details:** The "Rearing Tank Construction Scheme" by the Department of Agriculture, Animal Husbandry, and Cooperation (Fisheries Division), Government of Jharkhand, aims to support private-sector fish farming by constructing rearing tanks for sustainable fish production. Under this scheme, financial assistance is provided to beneficiaries for the construction of rearing ponds with a minimum water area of one acre.
- **Eligibility:** The applicant should be a fisherman. The applicant whose proposed land is near their residence, consisting of one, two, or three plots of "don" land. The applicant should be engaged in fish farming or have constructed a fish seed hatchery with a departmental subsidy. The land proposed for pond construction must be undisputed.  At least 130 decimals of land are required for a 100 decimal water area. For larger ponds, the ratio of water area to total land should be at least 1:1.3. The proposed land must not be mortgaged against any bank loan. The applicant must have valid possession of the proposed land and provide the necessary documentation. The applicant should be financially capable of contributing their share of the pond construction costs.
- **Benefits/scope:** Financial Assistance: SC/ST beneficiaries receive up to 80% of the total cost (maximum ₹4,00,000/-). Other categories receive up to 70% (maximum ₹3,50,000/-). Pond Construction Support: Assistance for constructing one-acre rearing ponds using machinery. Mode of Disbursement: Direct Benefit Transfer (DBT) to beneficiaries' bank accounts. Installments: First installment: ₹1,00,000 after one to two feet of excavation. Second installment: ₹2,00,000 after three feet of excavation. Remaining funds after full excavation and dressing verification.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 463
- **Candidate slug:** `bocs`
- **Scheme name/title:** Building And Other Construction Scholarship
- **Details:** Detailed Students who are pursuing technical or engineering education can apply online under the BOC Scholarship for getting the scholarship amounts. The student must belong to the SC category. Students must be pursuing his or her technical education at a recognized university. ﻿ The main objective of launching the BOC Scholarship is to provide scholarships to students pursuing technical education who have secured good or excellent merit records while carrying out their studies. This will provide social security provisions to the student belonging to the SC category or community. The student must be an ITI/ITC Polytechnic or Diploma. ﻿ Another objective of launching the BOC Scholarship is to provide social and economic welfare to the students so that they will be able to carry out their technical studies while getting the scholarship amount. The Department of Skill Development &amp; Technical Education will initiate all scholarship operations. ﻿
- **Eligibility:** The applicants will need to follow the mentioned eligibility criteria for getting online registration under this scholarship: – The student must be a permanent resident of Odisha. The student must belong to the SC category. The applicant must be pursuing technical education or ITI/Polytechnic courses. ﻿
- **Benefits/scope:** Benefits This scholarship offers various opportunities to SC-category students across the world. Under this scheme, the selected students will receive variable financial support from the Odisha government. Under the BOC scholarship, no living costs of the students are covered. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 44

- **Query text:** unorganized sector workers benefits
- **Original source label (unverified):** Building and Construction Workers Welfare Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 537
- **Candidate slug:** `cmbocwhrs`
- **Scheme name/title:** Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme
- **Details:** Launched in 2013, the scheme "Chief Minister's Building and Other Construction Workers Housing (Rural) Scheme" aims to provide permanent houses to registered construction workers in the rural areas of Madhya Pradesh who are homeless or living in kutcha/semi-pucca houses. This scheme is applicable in all rural areas of the state (excluding urban and Nazul outer areas).
- **Eligibility:** For Registration: The applicant should be a resident of Madhya Pradesh. The applicant should be a Building/ Construction Worker. The applicant should be between 18 and 60 years. The applicant should have engaged in any building or other construction work for at least 90 days during the preceding 12 months. The registration of the applicant should be renewed annually. For Application: The applicant should not fulfil the eligibility criteria for housing grants under Indira Awas Yojana or Chief Minister Antyodaya Awas Yojana. The applicant should have a family with a maximum of three hectares of agricultural land. The applicant's family's maximum income from all sources should be up to ₹3 lakh per annum. The applicant should have sufficient land available for house construction, as mentioned in clause 6 above. The applicant should be eligible to receive land for housing from the government. The applicant should be willing to construct a house on agricultural land owned by them. The applicant should be eligible to obtain a landholder certificate in the village population. The applicant should agree to obtain a bank loan for constructing a house with a 225 sq. ft. plinth area in the prescribed layout and provide their own contribution in the form of labour/material/inclusion.
- **Benefits/scope:** The Board reimburses a minimum loan grant of ₹50,000 to the beneficiary. The Banks may approve an additional loan of up to ₹30,000 based on repayment capacity, with no role for the State Government. The grant is limited to ₹50,000 per case. NOTE:  The Board provides the grant to District Labour Offices, which distribute it to banks based on approved loan cases.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2564
- **Candidate slug:** `rpcs`
- **Scheme name/title:** Rearing Pond Construction Scheme
- **Details:** The "Rearing Tank Construction Scheme" by the Department of Agriculture, Animal Husbandry, and Cooperation (Fisheries Division), Government of Jharkhand, aims to support private-sector fish farming by constructing rearing tanks for sustainable fish production. Under this scheme, financial assistance is provided to beneficiaries for the construction of rearing ponds with a minimum water area of one acre.
- **Eligibility:** The applicant should be a fisherman. The applicant whose proposed land is near their residence, consisting of one, two, or three plots of "don" land. The applicant should be engaged in fish farming or have constructed a fish seed hatchery with a departmental subsidy. The land proposed for pond construction must be undisputed.  At least 130 decimals of land are required for a 100 decimal water area. For larger ponds, the ratio of water area to total land should be at least 1:1.3. The proposed land must not be mortgaged against any bank loan. The applicant must have valid possession of the proposed land and provide the necessary documentation. The applicant should be financially capable of contributing their share of the pond construction costs.
- **Benefits/scope:** Financial Assistance: SC/ST beneficiaries receive up to 80% of the total cost (maximum ₹4,00,000/-). Other categories receive up to 70% (maximum ₹3,50,000/-). Pond Construction Support: Assistance for constructing one-acre rearing ponds using machinery. Mode of Disbursement: Direct Benefit Transfer (DBT) to beneficiaries' bank accounts. Installments: First installment: ₹1,00,000 after one to two feet of excavation. Second installment: ₹2,00,000 after three feet of excavation. Remaining funds after full excavation and dressing verification.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 463
- **Candidate slug:** `bocs`
- **Scheme name/title:** Building And Other Construction Scholarship
- **Details:** Detailed Students who are pursuing technical or engineering education can apply online under the BOC Scholarship for getting the scholarship amounts. The student must belong to the SC category. Students must be pursuing his or her technical education at a recognized university. ﻿ The main objective of launching the BOC Scholarship is to provide scholarships to students pursuing technical education who have secured good or excellent merit records while carrying out their studies. This will provide social security provisions to the student belonging to the SC category or community. The student must be an ITI/ITC Polytechnic or Diploma. ﻿ Another objective of launching the BOC Scholarship is to provide social and economic welfare to the students so that they will be able to carry out their technical studies while getting the scholarship amount. The Department of Skill Development &amp; Technical Education will initiate all scholarship operations. ﻿
- **Eligibility:** The applicants will need to follow the mentioned eligibility criteria for getting online registration under this scholarship: – The student must be a permanent resident of Odisha. The student must belong to the SC category. The applicant must be pursuing technical education or ITI/Polytechnic courses. ﻿
- **Benefits/scope:** Benefits This scholarship offers various opportunities to SC-category students across the world. Under this scheme, the selected students will receive variable financial support from the Odisha government. Under the BOC scholarship, no living costs of the students are covered. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 45

- **Query text:** fishermen welfare schemes
- **Original source label (unverified):** Welfare and Relief for Fishermen Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2182
- **Candidate slug:** `nswf`
- **Scheme name/title:** National Scheme Of Welfare Of Fishermen
- **Details:** The National Scheme of Welfare of Fishermen is a centrally sponsored scheme that provides financial assistance to fishermen. They can use these for constructing houses and community halls for both recreation and work purposes. Further, through the amount availed under this scheme, fishermen can install tube wells. ﻿ Objectives- ﻿ Provide fishermen with basic amenities such as housing, community halls, tube well for drinking water. Ensure Financial And Social Securities Of Fishermen And Their Families. Upgrade The Standard Of Living Of Fishermen. Educate And Train Fishermen In Advanced Technical Technologies So That They Can Learn Scientific Ways Of Fishing.
- **Eligibility:** Eligibility Criteria for Inland Fishermen ﻿ Fishermen living in coastal areas and with whom the respective States and Union Territories have officially licensed are eligible for this scheme. The age of fishermen must be below 60 years old. Applicant fishermen must belong to the BPL (Below Poverty Line) category. They must be engaged in full-time activities inland. ﻿ Eligibility Criteria for Marine Fishermen ﻿ All marine fishermen who operate under State, Union Territories, and FISHCOPFED are eligible for this government scheme for fishermen. However, there are other eligibility parameters marine fishermen must fulfill. These include - ﻿ Their respective States and Union Territories must officially license marine fishermen. They must involve themselves in full-time activities at sea. They must be a member of the Welfare Society or Federation or Cooperative Society. Please note that the fishermen under FISHCOPFED can avail of funds available under the insurance component only.
- **Benefits/scope:** Here are the features and benefits that this government scheme for fishermen offers - ﻿ Housing Facility The National Scheme of Welfare of Fishermen offers fishermen facilities for constructing houses. There is no upper limit for building homes in a particular village as it entirely depends on the number of fishermen residing. States through this scheme ensure equal distribution of houses among all fishermen. Also, this government-backed scheme dictates the house construction with a base area within 35 sq. mt. Also, the cost must not exceed ₹75,000. ﻿ Construction of Common Facility This government-backed scheme ensures building a community hall in some instances if there are more than 75 houses in a village. This scheme will build a community hall (with two toilets and a tube well) with a base area measuring 200 sq. mt. and within ₹2 lakh.  Fishermen can use this community hall as a mending shed and a drying yard. ﻿ Assurance of Clean Drinking Water This scheme offers a tube well for every 20 houses. Also, depending on the requirement, the number of tube wells is increased. In addition, this scheme provides an alternative option where tubewell installation is not possible. ﻿ Insurance Facility (For Group Accident Insurance for Active Fishermen)- This scheme provides fisherfolk or licensed or identified or registered with the States or Union Territory ₹50,000 in case of death or permanent total disability. Also, this scheme provides ₹25,000 for partial permanent disability. ﻿ Here, the insurance cover will continue for 12 months, and FISHCOPFED would take out a policy. Also, under this scheme, the affected fishermen will have to pay an annual premium worth ₹15 (per head). Here, the Central Government will pay 50%, and the State Government will pay the remaining 50% subsidy as grants-in-aid. In the case of Union Territories, the Central Government will bear a 100% premium. ﻿ On the other hand, those States/UT’s, which subscribed to this Group Accident Insurance for Active Fishermen through FISHCOPFED, will get a Central share of assistance (100% premium for Union Territories) directly through FISHCOPFED and not through States/UT’s. ﻿ Saving cum relief The National Scheme of Welfare of Fishermen further offers a savings cum relief scheme. This scheme component collects ₹75 from marine fishermen for 8 months in a year. Total ₹600 needs to be collected to match an equal amount worth ₹600 provided by the State and Central Government to segregate on a 50:50 basis. If any fishermen fail to make payment, the authorities will refund the paid amount with interest at the end of the 4th month. Also, the ‘lean months’ provisions vary from a coastal area or marine area, which FISHCOPFED decides entirely. ﻿ Now that individuals know about this government scheme for fishermen, i.e. the National Scheme of Welfare of Fishermen, they avail funds and construct houses of their own.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1092
- **Candidate slug:** `fars`
- **Scheme name/title:** Fishermen Accident Relief Scheme
- **Details:** The "Fishermen Accident Relief Scheme" introduced by the Agriculture, Farmers Welfare and Cooperation Department, Gujarat, aims to provide financial assistance to the families of deceased fishermen in Gujarat in case of death in Pakistan Jail, lost in the sea, or accidental death while fishing at sea. The financial assistance varies based on the cause of death and is meant to help the legal heirs cope with the loss.
- **Eligibility:** The applicant must be a legal heir of the deceased fisherman. The deceased must have been an active fisherman from Gujarat.
- **Benefits/scope:** ﻿ Name of Component Standard of Assistance Minimum Time Limit (in Years) for Reclaiming Benefits Death in Pakistan Jail ₹4,00,000/- Only once, after dead or lost declared as per rules. Lost in Sea ₹2,00,000/- Only once, after dead or lost declared as per rules. Accidental death while fishing at sea ₹2,00,000/- Only once, after dead or lost declared as per rules. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 709
- **Candidate slug:** `dvrsf`
- **Scheme name/title:** Diesel VAT Relief Scheme for Fishermen
- **Details:** The "Diesel VAT Relief Scheme for Fishermen" introduced by the Agriculture, Farmers Welfare and Cooperation Department, Gujarat, aims to support fishermen by subsidizing the VAT on diesel, making fuel more affordable for their mechanized boats. This helps reduce the operational cost of fishermen using mechanized boats.
- **Eligibility:** The applicant must be a registered diesel cardholder. The applicant must own a mechanized fishing boat. The boat should be less than 20 meters in length. ﻿ ﻿
- **Benefits/scope:** Name of Component Standard of Assistance Minimum Time Limit (in Years) for Reclaiming Benefits Diesel VAT assistance Per litre maximum assistance up to ₹15/- Assistance is available as per fixed diesel quota throughout the year
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 46

- **Query text:** fishing industry support government
- **Original source label (unverified):** Welfare and Relief for Fishermen Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2182
- **Candidate slug:** `nswf`
- **Scheme name/title:** National Scheme Of Welfare Of Fishermen
- **Details:** The National Scheme of Welfare of Fishermen is a centrally sponsored scheme that provides financial assistance to fishermen. They can use these for constructing houses and community halls for both recreation and work purposes. Further, through the amount availed under this scheme, fishermen can install tube wells. ﻿ Objectives- ﻿ Provide fishermen with basic amenities such as housing, community halls, tube well for drinking water. Ensure Financial And Social Securities Of Fishermen And Their Families. Upgrade The Standard Of Living Of Fishermen. Educate And Train Fishermen In Advanced Technical Technologies So That They Can Learn Scientific Ways Of Fishing.
- **Eligibility:** Eligibility Criteria for Inland Fishermen ﻿ Fishermen living in coastal areas and with whom the respective States and Union Territories have officially licensed are eligible for this scheme. The age of fishermen must be below 60 years old. Applicant fishermen must belong to the BPL (Below Poverty Line) category. They must be engaged in full-time activities inland. ﻿ Eligibility Criteria for Marine Fishermen ﻿ All marine fishermen who operate under State, Union Territories, and FISHCOPFED are eligible for this government scheme for fishermen. However, there are other eligibility parameters marine fishermen must fulfill. These include - ﻿ Their respective States and Union Territories must officially license marine fishermen. They must involve themselves in full-time activities at sea. They must be a member of the Welfare Society or Federation or Cooperative Society. Please note that the fishermen under FISHCOPFED can avail of funds available under the insurance component only.
- **Benefits/scope:** Here are the features and benefits that this government scheme for fishermen offers - ﻿ Housing Facility The National Scheme of Welfare of Fishermen offers fishermen facilities for constructing houses. There is no upper limit for building homes in a particular village as it entirely depends on the number of fishermen residing. States through this scheme ensure equal distribution of houses among all fishermen. Also, this government-backed scheme dictates the house construction with a base area within 35 sq. mt. Also, the cost must not exceed ₹75,000. ﻿ Construction of Common Facility This government-backed scheme ensures building a community hall in some instances if there are more than 75 houses in a village. This scheme will build a community hall (with two toilets and a tube well) with a base area measuring 200 sq. mt. and within ₹2 lakh.  Fishermen can use this community hall as a mending shed and a drying yard. ﻿ Assurance of Clean Drinking Water This scheme offers a tube well for every 20 houses. Also, depending on the requirement, the number of tube wells is increased. In addition, this scheme provides an alternative option where tubewell installation is not possible. ﻿ Insurance Facility (For Group Accident Insurance for Active Fishermen)- This scheme provides fisherfolk or licensed or identified or registered with the States or Union Territory ₹50,000 in case of death or permanent total disability. Also, this scheme provides ₹25,000 for partial permanent disability. ﻿ Here, the insurance cover will continue for 12 months, and FISHCOPFED would take out a policy. Also, under this scheme, the affected fishermen will have to pay an annual premium worth ₹15 (per head). Here, the Central Government will pay 50%, and the State Government will pay the remaining 50% subsidy as grants-in-aid. In the case of Union Territories, the Central Government will bear a 100% premium. ﻿ On the other hand, those States/UT’s, which subscribed to this Group Accident Insurance for Active Fishermen through FISHCOPFED, will get a Central share of assistance (100% premium for Union Territories) directly through FISHCOPFED and not through States/UT’s. ﻿ Saving cum relief The National Scheme of Welfare of Fishermen further offers a savings cum relief scheme. This scheme component collects ₹75 from marine fishermen for 8 months in a year. Total ₹600 needs to be collected to match an equal amount worth ₹600 provided by the State and Central Government to segregate on a 50:50 basis. If any fishermen fail to make payment, the authorities will refund the paid amount with interest at the end of the 4th month. Also, the ‘lean months’ provisions vary from a coastal area or marine area, which FISHCOPFED decides entirely. ﻿ Now that individuals know about this government scheme for fishermen, i.e. the National Scheme of Welfare of Fishermen, they avail funds and construct houses of their own.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1092
- **Candidate slug:** `fars`
- **Scheme name/title:** Fishermen Accident Relief Scheme
- **Details:** The "Fishermen Accident Relief Scheme" introduced by the Agriculture, Farmers Welfare and Cooperation Department, Gujarat, aims to provide financial assistance to the families of deceased fishermen in Gujarat in case of death in Pakistan Jail, lost in the sea, or accidental death while fishing at sea. The financial assistance varies based on the cause of death and is meant to help the legal heirs cope with the loss.
- **Eligibility:** The applicant must be a legal heir of the deceased fisherman. The deceased must have been an active fisherman from Gujarat.
- **Benefits/scope:** ﻿ Name of Component Standard of Assistance Minimum Time Limit (in Years) for Reclaiming Benefits Death in Pakistan Jail ₹4,00,000/- Only once, after dead or lost declared as per rules. Lost in Sea ₹2,00,000/- Only once, after dead or lost declared as per rules. Accidental death while fishing at sea ₹2,00,000/- Only once, after dead or lost declared as per rules. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 709
- **Candidate slug:** `dvrsf`
- **Scheme name/title:** Diesel VAT Relief Scheme for Fishermen
- **Details:** The "Diesel VAT Relief Scheme for Fishermen" introduced by the Agriculture, Farmers Welfare and Cooperation Department, Gujarat, aims to support fishermen by subsidizing the VAT on diesel, making fuel more affordable for their mechanized boats. This helps reduce the operational cost of fishermen using mechanized boats.
- **Eligibility:** The applicant must be a registered diesel cardholder. The applicant must own a mechanized fishing boat. The boat should be less than 20 meters in length. ﻿ ﻿
- **Benefits/scope:** Name of Component Standard of Assistance Minimum Time Limit (in Years) for Reclaiming Benefits Diesel VAT assistance Per litre maximum assistance up to ₹15/- Assistance is available as per fixed diesel quota throughout the year
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 47

- **Query text:** marine resources assistance
- **Original source label (unverified):** Welfare and Relief for Fishermen Scheme
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2182
- **Candidate slug:** `nswf`
- **Scheme name/title:** National Scheme Of Welfare Of Fishermen
- **Details:** The National Scheme of Welfare of Fishermen is a centrally sponsored scheme that provides financial assistance to fishermen. They can use these for constructing houses and community halls for both recreation and work purposes. Further, through the amount availed under this scheme, fishermen can install tube wells. ﻿ Objectives- ﻿ Provide fishermen with basic amenities such as housing, community halls, tube well for drinking water. Ensure Financial And Social Securities Of Fishermen And Their Families. Upgrade The Standard Of Living Of Fishermen. Educate And Train Fishermen In Advanced Technical Technologies So That They Can Learn Scientific Ways Of Fishing.
- **Eligibility:** Eligibility Criteria for Inland Fishermen ﻿ Fishermen living in coastal areas and with whom the respective States and Union Territories have officially licensed are eligible for this scheme. The age of fishermen must be below 60 years old. Applicant fishermen must belong to the BPL (Below Poverty Line) category. They must be engaged in full-time activities inland. ﻿ Eligibility Criteria for Marine Fishermen ﻿ All marine fishermen who operate under State, Union Territories, and FISHCOPFED are eligible for this government scheme for fishermen. However, there are other eligibility parameters marine fishermen must fulfill. These include - ﻿ Their respective States and Union Territories must officially license marine fishermen. They must involve themselves in full-time activities at sea. They must be a member of the Welfare Society or Federation or Cooperative Society. Please note that the fishermen under FISHCOPFED can avail of funds available under the insurance component only.
- **Benefits/scope:** Here are the features and benefits that this government scheme for fishermen offers - ﻿ Housing Facility The National Scheme of Welfare of Fishermen offers fishermen facilities for constructing houses. There is no upper limit for building homes in a particular village as it entirely depends on the number of fishermen residing. States through this scheme ensure equal distribution of houses among all fishermen. Also, this government-backed scheme dictates the house construction with a base area within 35 sq. mt. Also, the cost must not exceed ₹75,000. ﻿ Construction of Common Facility This government-backed scheme ensures building a community hall in some instances if there are more than 75 houses in a village. This scheme will build a community hall (with two toilets and a tube well) with a base area measuring 200 sq. mt. and within ₹2 lakh.  Fishermen can use this community hall as a mending shed and a drying yard. ﻿ Assurance of Clean Drinking Water This scheme offers a tube well for every 20 houses. Also, depending on the requirement, the number of tube wells is increased. In addition, this scheme provides an alternative option where tubewell installation is not possible. ﻿ Insurance Facility (For Group Accident Insurance for Active Fishermen)- This scheme provides fisherfolk or licensed or identified or registered with the States or Union Territory ₹50,000 in case of death or permanent total disability. Also, this scheme provides ₹25,000 for partial permanent disability. ﻿ Here, the insurance cover will continue for 12 months, and FISHCOPFED would take out a policy. Also, under this scheme, the affected fishermen will have to pay an annual premium worth ₹15 (per head). Here, the Central Government will pay 50%, and the State Government will pay the remaining 50% subsidy as grants-in-aid. In the case of Union Territories, the Central Government will bear a 100% premium. ﻿ On the other hand, those States/UT’s, which subscribed to this Group Accident Insurance for Active Fishermen through FISHCOPFED, will get a Central share of assistance (100% premium for Union Territories) directly through FISHCOPFED and not through States/UT’s. ﻿ Saving cum relief The National Scheme of Welfare of Fishermen further offers a savings cum relief scheme. This scheme component collects ₹75 from marine fishermen for 8 months in a year. Total ₹600 needs to be collected to match an equal amount worth ₹600 provided by the State and Central Government to segregate on a 50:50 basis. If any fishermen fail to make payment, the authorities will refund the paid amount with interest at the end of the 4th month. Also, the ‘lean months’ provisions vary from a coastal area or marine area, which FISHCOPFED decides entirely. ﻿ Now that individuals know about this government scheme for fishermen, i.e. the National Scheme of Welfare of Fishermen, they avail funds and construct houses of their own.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 1092
- **Candidate slug:** `fars`
- **Scheme name/title:** Fishermen Accident Relief Scheme
- **Details:** The "Fishermen Accident Relief Scheme" introduced by the Agriculture, Farmers Welfare and Cooperation Department, Gujarat, aims to provide financial assistance to the families of deceased fishermen in Gujarat in case of death in Pakistan Jail, lost in the sea, or accidental death while fishing at sea. The financial assistance varies based on the cause of death and is meant to help the legal heirs cope with the loss.
- **Eligibility:** The applicant must be a legal heir of the deceased fisherman. The deceased must have been an active fisherman from Gujarat.
- **Benefits/scope:** ﻿ Name of Component Standard of Assistance Minimum Time Limit (in Years) for Reclaiming Benefits Death in Pakistan Jail ₹4,00,000/- Only once, after dead or lost declared as per rules. Lost in Sea ₹2,00,000/- Only once, after dead or lost declared as per rules. Accidental death while fishing at sea ₹2,00,000/- Only once, after dead or lost declared as per rules. ﻿
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 709
- **Candidate slug:** `dvrsf`
- **Scheme name/title:** Diesel VAT Relief Scheme for Fishermen
- **Details:** The "Diesel VAT Relief Scheme for Fishermen" introduced by the Agriculture, Farmers Welfare and Cooperation Department, Gujarat, aims to support fishermen by subsidizing the VAT on diesel, making fuel more affordable for their mechanized boats. This helps reduce the operational cost of fishermen using mechanized boats.
- **Eligibility:** The applicant must be a registered diesel cardholder. The applicant must own a mechanized fishing boat. The boat should be less than 20 meters in length. ﻿ ﻿
- **Benefits/scope:** Name of Component Standard of Assistance Minimum Time Limit (in Years) for Reclaiming Benefits Diesel VAT assistance Per litre maximum assistance up to ₹15/- Assistance is available as per fixed diesel quota throughout the year
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 51

- **Query text:** micro finance for women
- **Original source label (unverified):** Pradhan Mantri Mahila Shakti Kendra
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2419
- **Candidate slug:** `pmgsy`
- **Scheme name/title:** Pradhan Mantri Gram Sadak Yojana
- **Details:** With the objective of providing rural connectivity, the Government of India launched the Pradhan Mantri Gram Sadak Yojana (referred to as PMGSY-I hereinafter) on 25th December 2000 to provide all-weather access to eligible unconnected habitations with a population of up to 500(Census 2001) in plain area and 250 and above in Special category States(States of North East, Jammu, and Kashmir, Himachal Pradesh, Uttarakhand), Desert Area as identified by Desert Development Program and 88 selected Backward Districts as identified by the Ministry of Home Affairs/Planning Commission as a strategy for poverty alleviation. ﻿ As of 8th December 2021, a total of 6,80,040 km of road length has been constructed under various interventions of Pradhan Mantri Gram Sadak Yojana (PMGSY). The primary objective of PMGSY concerns building robust, all-weather roads in rural habitations and other core areas. Panchayati Rajs and elected local representatives decide which habitations to be selected. This scheme was centrally funded only up to 2015-16. Since then, the funds have been divided between the Centre and the State. For North Eastern and Himalayan States (Jammu &amp; Kashmir, Uttarakhand, and Himachal Pradesh) 90% of a project is the Union Government funds, and 10% of this cost, is the State Government funds. For the Other States, the Union Government funds around 60% of a project while the remaining 40% is by State Government funds. ﻿ Some prominent features of PMGSY are - Proper decentralized planning for the building of roads. Build roads according to the Indian Road Congress and Rural Roads Manual. 3-tier quality management system. An unbroken flow of funds. ﻿ ﻿ ﻿ ﻿
- **Eligibility:** 1.  A region must be a habitation. It cannot be a hamlet or revenue village to be eligible for the Pradhan Mantri Gram Sadak Yojana (PMGSY). ﻿ 2.  The Central Government describes habitation as a population cluster residing within an area that remains constant over time. Some of the local words used to describe a habitation are: Majras, Desam, Hamlets, Tolas, Dhanis ﻿ 3.  The hamlet must have a higher population as per the 2001 Census to be eligible for road connection. The eligible habitations have a population of above 500 persons in plain areas and around 250 persons and above in hilly areas.
- **Benefits/scope:** The benefits of the Pradhan Mantri Gram Sadak Yojana (PMGSY) are - 1.  All-weather connection to the hamlets that are least or not connected. 2.  Overall Development of the country allows for easy movement of goods and vehicles. 3.  There are better employment opportunities for those from villages thanks to road connections.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2421
- **Candidate slug:** `pmjdy`
- **Scheme name/title:** Pradhan Mantri Jan Dhan Yojana
- **Details:** A  National Mission for Financial Inclusion (NMFI), namely, Pradhan Mantri Jan Dhan Yojana (PMJDY) was launched across the Country  in August, 2014 by the Prime Minister with the idea to ensure that citizens envisage their financial activities. PMJDY provides universal banking services for every unbanked household, based on the guiding principles of banking the unbanked, securing the unsecured, funding the unfunded and serving unserved and underserved areas. In order to give impetus to financial inclusion initiatives of the Government, PMJDY scheme was extended beyond 14.08.2018 with the focus on opening of accounts shifting from “every household” to “every unbanked adult”. The scheme has been made more attractive with upward revision in (i)	  OD limit from Rs. 5,000/- to Rs. 10,000/- and (ii)  Accidental  insurance cover on RuPay card holders from Rs.1 lakh to Rs.2 lakhs. PMJDY has been successful in increasing banking penetration and promoting financial inclusion across the country. The scheme has ensured access to various financial services like availability of basic savings bank account, access to need based credit, remittances facility, insurance and pension to the excluded sections i.e. weaker sections &amp; low-income groups.
- **Eligibility:** The applicant should be an Indian National. If minors above ten years apply, they will require support from their legal guardians for administering their PMJDY account.
- **Benefits/scope:** Basic Savings Bank Deposit Account (BSBDA) Any Indian citizen eligible to open a regular bank account can open a BSBDA. Such an account does not require any minimum balance maintenance. The account holders can use both bank branches, ATMs and Banking Correspondents (BCs) for depositing and withdrawing cash. However, one cannot withdraw cash more than four times a month. Small Account/Chota Khata Under Jan Dhan Yojana, people can open small bank accounts without presenting legal documents. These accounts would be valid normally for a period of twelve months. Thereafter, such accounts  would be allowed to a continue for a further period of twelve more months, if the account-holder provides a document showing that he/she has applied for any of the Officially Valid Document, within 12 months of opening the small account. RuPay Debit Card with inbuilt accident insurance Under PMJDY,  a free Rupay debit card,  with inbuilt accident insurance cover of Rs.2 lakhs (Rs 1 lakh for accounts opened before 28.08.2018),  is issued to all beneficiaries. Overdraft Facility Under PMJDY, beneficiaries can avail OD facility upto Rs. 10,000/-. Business Correspondents (BCs)/Bank Mitras  BCs/Bank Mitras are retail agents engaged by banks for providing banking services at locations other than a bank branch/ATM. It is mainly meant  for the rural areas, where bank branches are far-flung. BCs/Bank Mitras connect with the residents and guide them with banking solutions such as savings accounts, deposits, payments and withdrawals, mini account statements, etc. Banks with their strong network of BCs/Bank Mitras are providing hassle free services to the customers in remote / rural areas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 52

- **Query text:** women entrepreneurship support
- **Original source label (unverified):** Pradhan Mantri Mahila Shakti Kendra
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2419
- **Candidate slug:** `pmgsy`
- **Scheme name/title:** Pradhan Mantri Gram Sadak Yojana
- **Details:** With the objective of providing rural connectivity, the Government of India launched the Pradhan Mantri Gram Sadak Yojana (referred to as PMGSY-I hereinafter) on 25th December 2000 to provide all-weather access to eligible unconnected habitations with a population of up to 500(Census 2001) in plain area and 250 and above in Special category States(States of North East, Jammu, and Kashmir, Himachal Pradesh, Uttarakhand), Desert Area as identified by Desert Development Program and 88 selected Backward Districts as identified by the Ministry of Home Affairs/Planning Commission as a strategy for poverty alleviation. ﻿ As of 8th December 2021, a total of 6,80,040 km of road length has been constructed under various interventions of Pradhan Mantri Gram Sadak Yojana (PMGSY). The primary objective of PMGSY concerns building robust, all-weather roads in rural habitations and other core areas. Panchayati Rajs and elected local representatives decide which habitations to be selected. This scheme was centrally funded only up to 2015-16. Since then, the funds have been divided between the Centre and the State. For North Eastern and Himalayan States (Jammu &amp; Kashmir, Uttarakhand, and Himachal Pradesh) 90% of a project is the Union Government funds, and 10% of this cost, is the State Government funds. For the Other States, the Union Government funds around 60% of a project while the remaining 40% is by State Government funds. ﻿ Some prominent features of PMGSY are - Proper decentralized planning for the building of roads. Build roads according to the Indian Road Congress and Rural Roads Manual. 3-tier quality management system. An unbroken flow of funds. ﻿ ﻿ ﻿ ﻿
- **Eligibility:** 1.  A region must be a habitation. It cannot be a hamlet or revenue village to be eligible for the Pradhan Mantri Gram Sadak Yojana (PMGSY). ﻿ 2.  The Central Government describes habitation as a population cluster residing within an area that remains constant over time. Some of the local words used to describe a habitation are: Majras, Desam, Hamlets, Tolas, Dhanis ﻿ 3.  The hamlet must have a higher population as per the 2001 Census to be eligible for road connection. The eligible habitations have a population of above 500 persons in plain areas and around 250 persons and above in hilly areas.
- **Benefits/scope:** The benefits of the Pradhan Mantri Gram Sadak Yojana (PMGSY) are - 1.  All-weather connection to the hamlets that are least or not connected. 2.  Overall Development of the country allows for easy movement of goods and vehicles. 3.  There are better employment opportunities for those from villages thanks to road connections.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2421
- **Candidate slug:** `pmjdy`
- **Scheme name/title:** Pradhan Mantri Jan Dhan Yojana
- **Details:** A  National Mission for Financial Inclusion (NMFI), namely, Pradhan Mantri Jan Dhan Yojana (PMJDY) was launched across the Country  in August, 2014 by the Prime Minister with the idea to ensure that citizens envisage their financial activities. PMJDY provides universal banking services for every unbanked household, based on the guiding principles of banking the unbanked, securing the unsecured, funding the unfunded and serving unserved and underserved areas. In order to give impetus to financial inclusion initiatives of the Government, PMJDY scheme was extended beyond 14.08.2018 with the focus on opening of accounts shifting from “every household” to “every unbanked adult”. The scheme has been made more attractive with upward revision in (i)	  OD limit from Rs. 5,000/- to Rs. 10,000/- and (ii)  Accidental  insurance cover on RuPay card holders from Rs.1 lakh to Rs.2 lakhs. PMJDY has been successful in increasing banking penetration and promoting financial inclusion across the country. The scheme has ensured access to various financial services like availability of basic savings bank account, access to need based credit, remittances facility, insurance and pension to the excluded sections i.e. weaker sections &amp; low-income groups.
- **Eligibility:** The applicant should be an Indian National. If minors above ten years apply, they will require support from their legal guardians for administering their PMJDY account.
- **Benefits/scope:** Basic Savings Bank Deposit Account (BSBDA) Any Indian citizen eligible to open a regular bank account can open a BSBDA. Such an account does not require any minimum balance maintenance. The account holders can use both bank branches, ATMs and Banking Correspondents (BCs) for depositing and withdrawing cash. However, one cannot withdraw cash more than four times a month. Small Account/Chota Khata Under Jan Dhan Yojana, people can open small bank accounts without presenting legal documents. These accounts would be valid normally for a period of twelve months. Thereafter, such accounts  would be allowed to a continue for a further period of twelve more months, if the account-holder provides a document showing that he/she has applied for any of the Officially Valid Document, within 12 months of opening the small account. RuPay Debit Card with inbuilt accident insurance Under PMJDY,  a free Rupay debit card,  with inbuilt accident insurance cover of Rs.2 lakhs (Rs 1 lakh for accounts opened before 28.08.2018),  is issued to all beneficiaries. Overdraft Facility Under PMJDY, beneficiaries can avail OD facility upto Rs. 10,000/-. Business Correspondents (BCs)/Bank Mitras  BCs/Bank Mitras are retail agents engaged by banks for providing banking services at locations other than a bank branch/ATM. It is mainly meant  for the rural areas, where bank branches are far-flung. BCs/Bank Mitras connect with the residents and guide them with banking solutions such as savings accounts, deposits, payments and withdrawals, mini account statements, etc. Banks with their strong network of BCs/Bank Mitras are providing hassle free services to the customers in remote / rural areas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 53

- **Query text:** female business loan
- **Original source label (unverified):** Pradhan Mantri Mahila Shakti Kendra
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2419
- **Candidate slug:** `pmgsy`
- **Scheme name/title:** Pradhan Mantri Gram Sadak Yojana
- **Details:** With the objective of providing rural connectivity, the Government of India launched the Pradhan Mantri Gram Sadak Yojana (referred to as PMGSY-I hereinafter) on 25th December 2000 to provide all-weather access to eligible unconnected habitations with a population of up to 500(Census 2001) in plain area and 250 and above in Special category States(States of North East, Jammu, and Kashmir, Himachal Pradesh, Uttarakhand), Desert Area as identified by Desert Development Program and 88 selected Backward Districts as identified by the Ministry of Home Affairs/Planning Commission as a strategy for poverty alleviation. ﻿ As of 8th December 2021, a total of 6,80,040 km of road length has been constructed under various interventions of Pradhan Mantri Gram Sadak Yojana (PMGSY). The primary objective of PMGSY concerns building robust, all-weather roads in rural habitations and other core areas. Panchayati Rajs and elected local representatives decide which habitations to be selected. This scheme was centrally funded only up to 2015-16. Since then, the funds have been divided between the Centre and the State. For North Eastern and Himalayan States (Jammu &amp; Kashmir, Uttarakhand, and Himachal Pradesh) 90% of a project is the Union Government funds, and 10% of this cost, is the State Government funds. For the Other States, the Union Government funds around 60% of a project while the remaining 40% is by State Government funds. ﻿ Some prominent features of PMGSY are - Proper decentralized planning for the building of roads. Build roads according to the Indian Road Congress and Rural Roads Manual. 3-tier quality management system. An unbroken flow of funds. ﻿ ﻿ ﻿ ﻿
- **Eligibility:** 1.  A region must be a habitation. It cannot be a hamlet or revenue village to be eligible for the Pradhan Mantri Gram Sadak Yojana (PMGSY). ﻿ 2.  The Central Government describes habitation as a population cluster residing within an area that remains constant over time. Some of the local words used to describe a habitation are: Majras, Desam, Hamlets, Tolas, Dhanis ﻿ 3.  The hamlet must have a higher population as per the 2001 Census to be eligible for road connection. The eligible habitations have a population of above 500 persons in plain areas and around 250 persons and above in hilly areas.
- **Benefits/scope:** The benefits of the Pradhan Mantri Gram Sadak Yojana (PMGSY) are - 1.  All-weather connection to the hamlets that are least or not connected. 2.  Overall Development of the country allows for easy movement of goods and vehicles. 3.  There are better employment opportunities for those from villages thanks to road connections.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2421
- **Candidate slug:** `pmjdy`
- **Scheme name/title:** Pradhan Mantri Jan Dhan Yojana
- **Details:** A  National Mission for Financial Inclusion (NMFI), namely, Pradhan Mantri Jan Dhan Yojana (PMJDY) was launched across the Country  in August, 2014 by the Prime Minister with the idea to ensure that citizens envisage their financial activities. PMJDY provides universal banking services for every unbanked household, based on the guiding principles of banking the unbanked, securing the unsecured, funding the unfunded and serving unserved and underserved areas. In order to give impetus to financial inclusion initiatives of the Government, PMJDY scheme was extended beyond 14.08.2018 with the focus on opening of accounts shifting from “every household” to “every unbanked adult”. The scheme has been made more attractive with upward revision in (i)	  OD limit from Rs. 5,000/- to Rs. 10,000/- and (ii)  Accidental  insurance cover on RuPay card holders from Rs.1 lakh to Rs.2 lakhs. PMJDY has been successful in increasing banking penetration and promoting financial inclusion across the country. The scheme has ensured access to various financial services like availability of basic savings bank account, access to need based credit, remittances facility, insurance and pension to the excluded sections i.e. weaker sections &amp; low-income groups.
- **Eligibility:** The applicant should be an Indian National. If minors above ten years apply, they will require support from their legal guardians for administering their PMJDY account.
- **Benefits/scope:** Basic Savings Bank Deposit Account (BSBDA) Any Indian citizen eligible to open a regular bank account can open a BSBDA. Such an account does not require any minimum balance maintenance. The account holders can use both bank branches, ATMs and Banking Correspondents (BCs) for depositing and withdrawing cash. However, one cannot withdraw cash more than four times a month. Small Account/Chota Khata Under Jan Dhan Yojana, people can open small bank accounts without presenting legal documents. These accounts would be valid normally for a period of twelve months. Thereafter, such accounts  would be allowed to a continue for a further period of twelve more months, if the account-holder provides a document showing that he/she has applied for any of the Officially Valid Document, within 12 months of opening the small account. RuPay Debit Card with inbuilt accident insurance Under PMJDY,  a free Rupay debit card,  with inbuilt accident insurance cover of Rs.2 lakhs (Rs 1 lakh for accounts opened before 28.08.2018),  is issued to all beneficiaries. Overdraft Facility Under PMJDY, beneficiaries can avail OD facility upto Rs. 10,000/-. Business Correspondents (BCs)/Bank Mitras  BCs/Bank Mitras are retail agents engaged by banks for providing banking services at locations other than a bank branch/ATM. It is mainly meant  for the rural areas, where bank branches are far-flung. BCs/Bank Mitras connect with the residents and guide them with banking solutions such as savings accounts, deposits, payments and withdrawals, mini account statements, etc. Banks with their strong network of BCs/Bank Mitras are providing hassle free services to the customers in remote / rural areas.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 54

- **Query text:** education loan for college
- **Original source label (unverified):** Central Sector Scheme of Scholarship for College and University Students
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2433
- **Candidate slug:** `csss-cus`
- **Scheme name/title:** Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University students
- **Details:** "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students" is a Scholarship Scheme by the Department of Higher Education, Ministry of Education.  The primary objective of the scheme is to provide financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies. The scholarships are awarded based on the results of the Higher Secondary/ Class 12th Board Examination. A maximum of 82,000 fresh scholarships per annum are provided for pursuing Graduate/ Postgraduate degrees in colleges and universities and for professional courses, such as Medical, Engineering etc.
- **Eligibility:** The applicant must be above the 80th percentile of successful candidates in the relevant stream from the respective Board of Examination in Class 12th of 10+2 pattern or equivalent. The applicant must be pursuing regular degree courses. The applicant must be pursuing courses at colleges/ institutions recognized by the All India Council for Technical Education and the respective Regulatory Bodies concerned. The gross parental/ family income of the applicant should not exceed ₹4,50,000/- per annum. For renewal of scholarship in each year of study, besides getting at least 50% marks in the Annual Examination, maintenance of adequate attendance should be at least 75%. The students are required to have bank accounts opened, especially, in their name.
- **Benefits/scope:** Rate of Scholarship ₹12,000/-per annum at the Graduation level for the first three years of College and University courses. ₹20,000 per annum at the Post-graduation level. ₹20,000/-per annum in the 4th and 5th year to the Students pursuing professional courses, in case, where the duration of the course is five (5) years/Integrated course. Students pursuing technical courses such as B.Tech, B.Engg. will get scholarship up to graduation level only i.e. ₹12,000 p.a. for 1st, 2nd, and 3rd year and ₹20,000 in the 4th year. ﻿ Mode of Disbursal The scholarship will be disbursed directly into the savings bank accounts of the beneficiaries through Direct Benefit Transfer (DBT).
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 500
- **Candidate slug:** `pmsoeds`
- **Scheme name/title:** Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India
- **Details:** The "Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India" aims at providing financial assistance to students from the Backward Classes (BC), Economically Weaker Sections (EWS), and Denotified, Nomadic, and Denotified, Nomadic Tribes (DNTs) to pursue higher education. This scholarship aims to alleviate the financial burden on students belonging to these marginalized communities, enabling them to continue their studies and enhance their skills. The scholarship covers tuition fees, maintenance allowances, and other academic expenses. The financial support is extended to students studying in both government and private institutions.
- **Eligibility:** The applicant should be from Other Backward Classes (OBC) / Economically Backward Classes (EBC) or from Denotified, Nomadic, and Semi-Nomadic Tribes (DNT). The applicant should be studying at the post-matriculation or post-secondary stage of education. The applicant should be permanently settled in the State/UT where they are applying. The applicant should be studying in an institution recognized by the All India Survey on Higher Education (AISHE) or Unified District Information System for Education (UDISE). The applicant's institution should have National Assessment and Accreditation Council (NAAC) or National Board of Accreditation (NBA) accreditation. The applicant should maintain Aadhaar-based attendance in the institution. The applicant must have a valid "Freeship Card" issued by the State/District Authority. Preference/Priority/Reservation/Relaxation: A maximum of 20 slots per annum are reserved for Commercial Pilot License courses, including helicopter and multi-engine training.
- **Benefits/scope:** Components of the Scholarship Maintenance allowance for the complete duration of the course. Reimbursement of compulsory non-refundable fees. Study tour charges (if applicable). Thesis typing/printing charges (for research scholars). Book allowance for students pursuing correspondence courses. Additional allowances for students with disabilities. Financial Support Breakdown Category of Courses Academic Allowance (Yearly in ₹) Tuition Fee (Yearly in ₹) Total (Yearly in ₹) Group 1: Degree and Post Graduate level professional courses 10,000 10,000 20,000 Group 2: Other Professional Courses leading to Degree, Diploma, Certificate 8,000 5,000 13,000 Group 3: Graduate and Post Graduate courses not covered under Group 1 &amp; Group 2 6,000 2,000 8,000 Group 4: All post-matriculation (Post Class X level) non-degree courses 5,000 0 5,000 *Students pursuing C.A./I.C.W.A./C.S./I.C.F.A. shall be treated as day scholars for academic allowance purposes. *Students studying through correspondence/online courses shall not be eligible for academic allowance. *Tuition fees shall be paid to online/correspondence students. *The State Governments may, if they decide, top up the academic allowance from their own resources. *The scholarship amount will be disbursed annually to the bank account of the beneficiary. *The scholarship continues for the duration of the course, subject to satisfactory academic progress.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2174
- **Candidate slug:** `css-nos-st`
- **Scheme name/title:** National Overseas Scholarship For Scheduled Tribes (ST) Students
- **Details:** A scholarship scheme by the Ministry of Tribal Affairs for regular, full-time students from Scheduled Tribes, to obtain higher education (post-graduate courses viz. Masters, Ph.D. and Post-Doctoral Research) from foreign institutes/universities. The Scheme is implemented through the Indian Embassies/Missions abroad, Ministry of External Affairs. 30% of the scholarship awards are earmarked for female candidates. Bachelor-level courses in any discipline are not covered under the scheme. Financial assistance is provided till completion of the course/research or the prescribed duration of the course, whichever is earlier. Selection is based on Interview based merit list prepared by An Expert Committee. The Scholarship comprises of tuition fee, Annual Maintenance allowance of USD 15400, Contingency Charges of USD 1532, Poll Tax, Visa Fee, Medical Insurance, Cost of Air journey, Incidental Journey expenses. The fields of study covered in this scheme are -: Pure/Applied Science/Engineering/Technology/Mathematics(STEM), Management, Economics, Finance, Law, Agriculture/Medicine, Humanities/Social Science/Fine Arts. Number of Award: 20 awards every year would be sanctioned to ST students as under: Sl. No Category No. of Award 1. Scheduled Tribes (ST) candidates 17 2. Particularly Vulnerable Tribal Groups (PVTG) 03 ﻿ Total 20 Subjects and Slots covered under the Scheme: The subjects/disciplines in which student can opt for studies abroad and the number of slots available under each field for grant of award are listed below: - Field of study Number of slots for the field of study Pure/Applied Science/ Engineering/Technology/ Mathematics (STEM) 10 Management, Economics, Finance, Law 04 Agriculture/Medicine 04 Humanities/Social Science/Fine Arts 02 Duration of award with Financial Assistance: Financial assistance will be provided till completion of the course/research or the prescribed duration of the course, whichever is earlier: - Sl. No Course Maximum Duration 1. Post-Doctoral Research 2 years 2. Ph. D 4 years (four years) 3. Master's Degree 1 or 2 years (One/Two years) depending upon the type and duration of the Course.
- **Eligibility:** The applicant must be from a Scheduled Tribe (ST). The applicant must be pursuing a post-graduate course (Master, Ph.D., or Post-Doctoral Research) from a foreign institute/university. The annual income of the family of the applicant (from all sources) should not be greater than ₹ 6,00,000/-. The applicant must have secured at least 55% marks or equivalent grade in the qualifying examination (In the case of Post-Doctoral Research, the qualifying exam is Ph.D.; In the case of Ph.D., the qualifying exam is a Master’s Degree; In the case of a Master’s Degree, the qualifying exam is a Bachelor's Degree) The applicant must be the only child in the family who is availing/has availed of this scholarship. Age Criteria:- If pursuing Post-Doctoral Research, the age of the applicant as on 1st July of the selection year, should not be greater than 38 years. If pursuing Ph.D., the age of the applicant as on 1st July of the selection year, should not be greater than 35 years. If pursuing Masters, the age of the applicant as on 1st July of the selection year, should not be greater than 32 years. Income Criteria:- Scholarships will be paid to the students whose family income from all sources does not exceed ₹ 6,00,000/- (Rupees Six lakhs only) per annum. The family income shall be computed in the following manner: - In case where both father and mother are working, the combined income of both of them from all sources shall be taken into account in computing total family income. In case any other member of the family, other than father and mother, is an earning member, his or her income shall not be included in computing total family income. In case only one parent is alive, the income of that parent shall be taken into account for considering total family income. If other sibling or family member is an earning member, their income shall not be included in computing total family income. In case of an orphan, supported by a guardian, income criteria shall not apply. Note:- 30% of the awards for each year shall be earmarked for women candidates. However, in case, adequate women candidates are not available as per the stipulations of the scheme, then the unutilized slots will be utilized by selecting suitable male candidates. There are 17 slots for ST candidates and 3 slots for PVTG candidates. An individual is eligible for only one award and cannot be considered for any other award or same/higher level of award for the second time under the Scheme. Other Conditions:- Selected candidates shall furnish all such documents and enter into such agreements before their departure as shall be decided by the Government of India from time to time. In case the candidate is already residing abroad, he/she shall furnish all relevant documents and enter into such agreements prior to the release of the scholarship by the Indian Mission. The candidate shall not change the course of study or research and the Institute for which scholarship has been sanctioned. It will be the responsibility of candidate to obtain the appropriate visa for a country wherein he/she intends to study. In case the awardee has received overpayment through Indian Mission abroad or any other Government agency, he/she shall refund the same to Indian Mission abroad. After completion of the course, the awardee shall upload the course completion details along with brief of study in the Alumni Module of National Overseas Scholarship (NOS) portal of the Ministry before his return tickets are booked. Criteria for preparation of Merit List:- All applications received within the stipulated period, will be scrutinized for the eligibility criteria. Separate merit list will be drawn for each field of study. The eligible applications will be considered for award of scholarship as per the procedure given below: First priority will be given to the candidates who have already got admission and are pursuing their studies in the top 1,000 ranked foreign Institutes/Universities (as per the latest QS world ranking). The merit list will be drawn based on the ranking of the Institute. In case of a tie between the QS rankings of two or more candidates, merit will be decided on the basis of marks/grades secured by the candidate in the qualifying examination for higher studies for which the scholarship has been applied for. In case sufficient number of students are not selected as mentioned in para (a) above, merit list will be drawn from the candidates who have already secured preliminary letter/offer of admission from top 1,000 ranked foreign Institutes/Universities (as per the QS world ranking) and are yet to join. Merit list will be drawn in similar manner as mentioned in para ‘a’ above; i.e. based on the ranking of the Institute and in case of tie in ranking of university/institution, the marks/grades secured by the candidate in the qualifying examination. In case sufficient students are not selected as per para “1” and “2” above, the vacant slots will be filled from among the remaining eligible candidates through personal interview by a committee of experts constituted by the Ministry. The candidates who have cleared GRE/GMAT/TOFEL etc. will be given preference.
- **Benefits/scope:** ﻿ Sl. No. Scholarship Component Details 1. Annual Maintenance Allowance The Annual maintenance allowance in USD15,400 ($ Fifteen thousand four hundred only) in US/ Pound sterling 9,900 (£ Nine thousand nine hundred only) in United Kingdom for all level courses. For other countries, the USD or equivalent rates would be applicable. 2. Annual Contingency and Equipment Allowance The Annual Contingency and Equipment Allowance for books/essential apparatus/study tour/typing and binding of thesis etc. will be $ 1532 (US Dollars One thousand five hundred thirty-two only) for the candidates in US and for candidates in United Kingdom, it will be £ 1116 (Pounds sterling One thousand one hundred sixteen only). For other countries, US Dollar or equivalent rates would be applicable. 3. Poll Tax Actuals shall be paid, wherever applicable. 4. Visa Fees Actual visa fees in Indian Rupees will be paid. 5. Incidental Journey Expenses Incidental journey expenses up to US Dollars 20 or its equivalent in Indian Rupees are permissible. 6. Fees Tuition fees and other non-refundable fees which is required to be compulsorily paid by the student for completion of the course, as per actuals. 7. Medical Insurance Premium Actuals as charged will be admissible. The Indian Embassy/Mission in the respective country will however examine the reasonableness of medical premium opted/claimed by the student. 8. Cost of Air Passage Air passage grant on actual basis from India to the nearest place to the educational institution and back to India, by economy class and shortest route at best available price shall be provided. 9. Local Travel Second class railway fare from the port of disembarkation to the place of study and back; in case of far flung places not connected by rail, bus fare from the place of residence to the nearest railway station, actual charge of crossing by ferry, air fare to the nearest rail-cum-air Station will be permissible. Note: Extension of stay beyond prescribed duration for levels of courses as mentioned above, will be without financial assistance of any kind except the air passage to return to India, if the candidate decides to come back to India on completion of the course.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 55

- **Query text:** student financial aid government
- **Original source label (unverified):** Central Sector Scheme of Scholarship for College and University Students
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2433
- **Candidate slug:** `csss-cus`
- **Scheme name/title:** Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University students
- **Details:** "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students" is a Scholarship Scheme by the Department of Higher Education, Ministry of Education.  The primary objective of the scheme is to provide financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies. The scholarships are awarded based on the results of the Higher Secondary/ Class 12th Board Examination. A maximum of 82,000 fresh scholarships per annum are provided for pursuing Graduate/ Postgraduate degrees in colleges and universities and for professional courses, such as Medical, Engineering etc.
- **Eligibility:** The applicant must be above the 80th percentile of successful candidates in the relevant stream from the respective Board of Examination in Class 12th of 10+2 pattern or equivalent. The applicant must be pursuing regular degree courses. The applicant must be pursuing courses at colleges/ institutions recognized by the All India Council for Technical Education and the respective Regulatory Bodies concerned. The gross parental/ family income of the applicant should not exceed ₹4,50,000/- per annum. For renewal of scholarship in each year of study, besides getting at least 50% marks in the Annual Examination, maintenance of adequate attendance should be at least 75%. The students are required to have bank accounts opened, especially, in their name.
- **Benefits/scope:** Rate of Scholarship ₹12,000/-per annum at the Graduation level for the first three years of College and University courses. ₹20,000 per annum at the Post-graduation level. ₹20,000/-per annum in the 4th and 5th year to the Students pursuing professional courses, in case, where the duration of the course is five (5) years/Integrated course. Students pursuing technical courses such as B.Tech, B.Engg. will get scholarship up to graduation level only i.e. ₹12,000 p.a. for 1st, 2nd, and 3rd year and ₹20,000 in the 4th year. ﻿ Mode of Disbursal The scholarship will be disbursed directly into the savings bank accounts of the beneficiaries through Direct Benefit Transfer (DBT).
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 500
- **Candidate slug:** `pmsoeds`
- **Scheme name/title:** Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India
- **Details:** The "Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India" aims at providing financial assistance to students from the Backward Classes (BC), Economically Weaker Sections (EWS), and Denotified, Nomadic, and Denotified, Nomadic Tribes (DNTs) to pursue higher education. This scholarship aims to alleviate the financial burden on students belonging to these marginalized communities, enabling them to continue their studies and enhance their skills. The scholarship covers tuition fees, maintenance allowances, and other academic expenses. The financial support is extended to students studying in both government and private institutions.
- **Eligibility:** The applicant should be from Other Backward Classes (OBC) / Economically Backward Classes (EBC) or from Denotified, Nomadic, and Semi-Nomadic Tribes (DNT). The applicant should be studying at the post-matriculation or post-secondary stage of education. The applicant should be permanently settled in the State/UT where they are applying. The applicant should be studying in an institution recognized by the All India Survey on Higher Education (AISHE) or Unified District Information System for Education (UDISE). The applicant's institution should have National Assessment and Accreditation Council (NAAC) or National Board of Accreditation (NBA) accreditation. The applicant should maintain Aadhaar-based attendance in the institution. The applicant must have a valid "Freeship Card" issued by the State/District Authority. Preference/Priority/Reservation/Relaxation: A maximum of 20 slots per annum are reserved for Commercial Pilot License courses, including helicopter and multi-engine training.
- **Benefits/scope:** Components of the Scholarship Maintenance allowance for the complete duration of the course. Reimbursement of compulsory non-refundable fees. Study tour charges (if applicable). Thesis typing/printing charges (for research scholars). Book allowance for students pursuing correspondence courses. Additional allowances for students with disabilities. Financial Support Breakdown Category of Courses Academic Allowance (Yearly in ₹) Tuition Fee (Yearly in ₹) Total (Yearly in ₹) Group 1: Degree and Post Graduate level professional courses 10,000 10,000 20,000 Group 2: Other Professional Courses leading to Degree, Diploma, Certificate 8,000 5,000 13,000 Group 3: Graduate and Post Graduate courses not covered under Group 1 &amp; Group 2 6,000 2,000 8,000 Group 4: All post-matriculation (Post Class X level) non-degree courses 5,000 0 5,000 *Students pursuing C.A./I.C.W.A./C.S./I.C.F.A. shall be treated as day scholars for academic allowance purposes. *Students studying through correspondence/online courses shall not be eligible for academic allowance. *Tuition fees shall be paid to online/correspondence students. *The State Governments may, if they decide, top up the academic allowance from their own resources. *The scholarship amount will be disbursed annually to the bank account of the beneficiary. *The scholarship continues for the duration of the course, subject to satisfactory academic progress.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2174
- **Candidate slug:** `css-nos-st`
- **Scheme name/title:** National Overseas Scholarship For Scheduled Tribes (ST) Students
- **Details:** A scholarship scheme by the Ministry of Tribal Affairs for regular, full-time students from Scheduled Tribes, to obtain higher education (post-graduate courses viz. Masters, Ph.D. and Post-Doctoral Research) from foreign institutes/universities. The Scheme is implemented through the Indian Embassies/Missions abroad, Ministry of External Affairs. 30% of the scholarship awards are earmarked for female candidates. Bachelor-level courses in any discipline are not covered under the scheme. Financial assistance is provided till completion of the course/research or the prescribed duration of the course, whichever is earlier. Selection is based on Interview based merit list prepared by An Expert Committee. The Scholarship comprises of tuition fee, Annual Maintenance allowance of USD 15400, Contingency Charges of USD 1532, Poll Tax, Visa Fee, Medical Insurance, Cost of Air journey, Incidental Journey expenses. The fields of study covered in this scheme are -: Pure/Applied Science/Engineering/Technology/Mathematics(STEM), Management, Economics, Finance, Law, Agriculture/Medicine, Humanities/Social Science/Fine Arts. Number of Award: 20 awards every year would be sanctioned to ST students as under: Sl. No Category No. of Award 1. Scheduled Tribes (ST) candidates 17 2. Particularly Vulnerable Tribal Groups (PVTG) 03 ﻿ Total 20 Subjects and Slots covered under the Scheme: The subjects/disciplines in which student can opt for studies abroad and the number of slots available under each field for grant of award are listed below: - Field of study Number of slots for the field of study Pure/Applied Science/ Engineering/Technology/ Mathematics (STEM) 10 Management, Economics, Finance, Law 04 Agriculture/Medicine 04 Humanities/Social Science/Fine Arts 02 Duration of award with Financial Assistance: Financial assistance will be provided till completion of the course/research or the prescribed duration of the course, whichever is earlier: - Sl. No Course Maximum Duration 1. Post-Doctoral Research 2 years 2. Ph. D 4 years (four years) 3. Master's Degree 1 or 2 years (One/Two years) depending upon the type and duration of the Course.
- **Eligibility:** The applicant must be from a Scheduled Tribe (ST). The applicant must be pursuing a post-graduate course (Master, Ph.D., or Post-Doctoral Research) from a foreign institute/university. The annual income of the family of the applicant (from all sources) should not be greater than ₹ 6,00,000/-. The applicant must have secured at least 55% marks or equivalent grade in the qualifying examination (In the case of Post-Doctoral Research, the qualifying exam is Ph.D.; In the case of Ph.D., the qualifying exam is a Master’s Degree; In the case of a Master’s Degree, the qualifying exam is a Bachelor's Degree) The applicant must be the only child in the family who is availing/has availed of this scholarship. Age Criteria:- If pursuing Post-Doctoral Research, the age of the applicant as on 1st July of the selection year, should not be greater than 38 years. If pursuing Ph.D., the age of the applicant as on 1st July of the selection year, should not be greater than 35 years. If pursuing Masters, the age of the applicant as on 1st July of the selection year, should not be greater than 32 years. Income Criteria:- Scholarships will be paid to the students whose family income from all sources does not exceed ₹ 6,00,000/- (Rupees Six lakhs only) per annum. The family income shall be computed in the following manner: - In case where both father and mother are working, the combined income of both of them from all sources shall be taken into account in computing total family income. In case any other member of the family, other than father and mother, is an earning member, his or her income shall not be included in computing total family income. In case only one parent is alive, the income of that parent shall be taken into account for considering total family income. If other sibling or family member is an earning member, their income shall not be included in computing total family income. In case of an orphan, supported by a guardian, income criteria shall not apply. Note:- 30% of the awards for each year shall be earmarked for women candidates. However, in case, adequate women candidates are not available as per the stipulations of the scheme, then the unutilized slots will be utilized by selecting suitable male candidates. There are 17 slots for ST candidates and 3 slots for PVTG candidates. An individual is eligible for only one award and cannot be considered for any other award or same/higher level of award for the second time under the Scheme. Other Conditions:- Selected candidates shall furnish all such documents and enter into such agreements before their departure as shall be decided by the Government of India from time to time. In case the candidate is already residing abroad, he/she shall furnish all relevant documents and enter into such agreements prior to the release of the scholarship by the Indian Mission. The candidate shall not change the course of study or research and the Institute for which scholarship has been sanctioned. It will be the responsibility of candidate to obtain the appropriate visa for a country wherein he/she intends to study. In case the awardee has received overpayment through Indian Mission abroad or any other Government agency, he/she shall refund the same to Indian Mission abroad. After completion of the course, the awardee shall upload the course completion details along with brief of study in the Alumni Module of National Overseas Scholarship (NOS) portal of the Ministry before his return tickets are booked. Criteria for preparation of Merit List:- All applications received within the stipulated period, will be scrutinized for the eligibility criteria. Separate merit list will be drawn for each field of study. The eligible applications will be considered for award of scholarship as per the procedure given below: First priority will be given to the candidates who have already got admission and are pursuing their studies in the top 1,000 ranked foreign Institutes/Universities (as per the latest QS world ranking). The merit list will be drawn based on the ranking of the Institute. In case of a tie between the QS rankings of two or more candidates, merit will be decided on the basis of marks/grades secured by the candidate in the qualifying examination for higher studies for which the scholarship has been applied for. In case sufficient number of students are not selected as mentioned in para (a) above, merit list will be drawn from the candidates who have already secured preliminary letter/offer of admission from top 1,000 ranked foreign Institutes/Universities (as per the QS world ranking) and are yet to join. Merit list will be drawn in similar manner as mentioned in para ‘a’ above; i.e. based on the ranking of the Institute and in case of tie in ranking of university/institution, the marks/grades secured by the candidate in the qualifying examination. In case sufficient students are not selected as per para “1” and “2” above, the vacant slots will be filled from among the remaining eligible candidates through personal interview by a committee of experts constituted by the Ministry. The candidates who have cleared GRE/GMAT/TOFEL etc. will be given preference.
- **Benefits/scope:** ﻿ Sl. No. Scholarship Component Details 1. Annual Maintenance Allowance The Annual maintenance allowance in USD15,400 ($ Fifteen thousand four hundred only) in US/ Pound sterling 9,900 (£ Nine thousand nine hundred only) in United Kingdom for all level courses. For other countries, the USD or equivalent rates would be applicable. 2. Annual Contingency and Equipment Allowance The Annual Contingency and Equipment Allowance for books/essential apparatus/study tour/typing and binding of thesis etc. will be $ 1532 (US Dollars One thousand five hundred thirty-two only) for the candidates in US and for candidates in United Kingdom, it will be £ 1116 (Pounds sterling One thousand one hundred sixteen only). For other countries, US Dollar or equivalent rates would be applicable. 3. Poll Tax Actuals shall be paid, wherever applicable. 4. Visa Fees Actual visa fees in Indian Rupees will be paid. 5. Incidental Journey Expenses Incidental journey expenses up to US Dollars 20 or its equivalent in Indian Rupees are permissible. 6. Fees Tuition fees and other non-refundable fees which is required to be compulsorily paid by the student for completion of the course, as per actuals. 7. Medical Insurance Premium Actuals as charged will be admissible. The Indian Embassy/Mission in the respective country will however examine the reasonableness of medical premium opted/claimed by the student. 8. Cost of Air Passage Air passage grant on actual basis from India to the nearest place to the educational institution and back to India, by economy class and shortest route at best available price shall be provided. 9. Local Travel Second class railway fare from the port of disembarkation to the place of study and back; in case of far flung places not connected by rail, bus fare from the place of residence to the nearest railway station, actual charge of crossing by ferry, air fare to the nearest rail-cum-air Station will be permissible. Note: Extension of stay beyond prescribed duration for levels of courses as mentioned above, will be without financial assistance of any kind except the air passage to return to India, if the candidate decides to come back to India on completion of the course.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 56

- **Query text:** higher education assistance
- **Original source label (unverified):** Central Sector Scheme of Scholarship for College and University Students
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2433
- **Candidate slug:** `csss-cus`
- **Scheme name/title:** Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University students
- **Details:** "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students" is a Scholarship Scheme by the Department of Higher Education, Ministry of Education.  The primary objective of the scheme is to provide financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies. The scholarships are awarded based on the results of the Higher Secondary/ Class 12th Board Examination. A maximum of 82,000 fresh scholarships per annum are provided for pursuing Graduate/ Postgraduate degrees in colleges and universities and for professional courses, such as Medical, Engineering etc.
- **Eligibility:** The applicant must be above the 80th percentile of successful candidates in the relevant stream from the respective Board of Examination in Class 12th of 10+2 pattern or equivalent. The applicant must be pursuing regular degree courses. The applicant must be pursuing courses at colleges/ institutions recognized by the All India Council for Technical Education and the respective Regulatory Bodies concerned. The gross parental/ family income of the applicant should not exceed ₹4,50,000/- per annum. For renewal of scholarship in each year of study, besides getting at least 50% marks in the Annual Examination, maintenance of adequate attendance should be at least 75%. The students are required to have bank accounts opened, especially, in their name.
- **Benefits/scope:** Rate of Scholarship ₹12,000/-per annum at the Graduation level for the first three years of College and University courses. ₹20,000 per annum at the Post-graduation level. ₹20,000/-per annum in the 4th and 5th year to the Students pursuing professional courses, in case, where the duration of the course is five (5) years/Integrated course. Students pursuing technical courses such as B.Tech, B.Engg. will get scholarship up to graduation level only i.e. ₹12,000 p.a. for 1st, 2nd, and 3rd year and ₹20,000 in the 4th year. ﻿ Mode of Disbursal The scholarship will be disbursed directly into the savings bank accounts of the beneficiaries through Direct Benefit Transfer (DBT).
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 500
- **Candidate slug:** `pmsoeds`
- **Scheme name/title:** Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India
- **Details:** The "Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India" aims at providing financial assistance to students from the Backward Classes (BC), Economically Weaker Sections (EWS), and Denotified, Nomadic, and Denotified, Nomadic Tribes (DNTs) to pursue higher education. This scholarship aims to alleviate the financial burden on students belonging to these marginalized communities, enabling them to continue their studies and enhance their skills. The scholarship covers tuition fees, maintenance allowances, and other academic expenses. The financial support is extended to students studying in both government and private institutions.
- **Eligibility:** The applicant should be from Other Backward Classes (OBC) / Economically Backward Classes (EBC) or from Denotified, Nomadic, and Semi-Nomadic Tribes (DNT). The applicant should be studying at the post-matriculation or post-secondary stage of education. The applicant should be permanently settled in the State/UT where they are applying. The applicant should be studying in an institution recognized by the All India Survey on Higher Education (AISHE) or Unified District Information System for Education (UDISE). The applicant's institution should have National Assessment and Accreditation Council (NAAC) or National Board of Accreditation (NBA) accreditation. The applicant should maintain Aadhaar-based attendance in the institution. The applicant must have a valid "Freeship Card" issued by the State/District Authority. Preference/Priority/Reservation/Relaxation: A maximum of 20 slots per annum are reserved for Commercial Pilot License courses, including helicopter and multi-engine training.
- **Benefits/scope:** Components of the Scholarship Maintenance allowance for the complete duration of the course. Reimbursement of compulsory non-refundable fees. Study tour charges (if applicable). Thesis typing/printing charges (for research scholars). Book allowance for students pursuing correspondence courses. Additional allowances for students with disabilities. Financial Support Breakdown Category of Courses Academic Allowance (Yearly in ₹) Tuition Fee (Yearly in ₹) Total (Yearly in ₹) Group 1: Degree and Post Graduate level professional courses 10,000 10,000 20,000 Group 2: Other Professional Courses leading to Degree, Diploma, Certificate 8,000 5,000 13,000 Group 3: Graduate and Post Graduate courses not covered under Group 1 &amp; Group 2 6,000 2,000 8,000 Group 4: All post-matriculation (Post Class X level) non-degree courses 5,000 0 5,000 *Students pursuing C.A./I.C.W.A./C.S./I.C.F.A. shall be treated as day scholars for academic allowance purposes. *Students studying through correspondence/online courses shall not be eligible for academic allowance. *Tuition fees shall be paid to online/correspondence students. *The State Governments may, if they decide, top up the academic allowance from their own resources. *The scholarship amount will be disbursed annually to the bank account of the beneficiary. *The scholarship continues for the duration of the course, subject to satisfactory academic progress.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2174
- **Candidate slug:** `css-nos-st`
- **Scheme name/title:** National Overseas Scholarship For Scheduled Tribes (ST) Students
- **Details:** A scholarship scheme by the Ministry of Tribal Affairs for regular, full-time students from Scheduled Tribes, to obtain higher education (post-graduate courses viz. Masters, Ph.D. and Post-Doctoral Research) from foreign institutes/universities. The Scheme is implemented through the Indian Embassies/Missions abroad, Ministry of External Affairs. 30% of the scholarship awards are earmarked for female candidates. Bachelor-level courses in any discipline are not covered under the scheme. Financial assistance is provided till completion of the course/research or the prescribed duration of the course, whichever is earlier. Selection is based on Interview based merit list prepared by An Expert Committee. The Scholarship comprises of tuition fee, Annual Maintenance allowance of USD 15400, Contingency Charges of USD 1532, Poll Tax, Visa Fee, Medical Insurance, Cost of Air journey, Incidental Journey expenses. The fields of study covered in this scheme are -: Pure/Applied Science/Engineering/Technology/Mathematics(STEM), Management, Economics, Finance, Law, Agriculture/Medicine, Humanities/Social Science/Fine Arts. Number of Award: 20 awards every year would be sanctioned to ST students as under: Sl. No Category No. of Award 1. Scheduled Tribes (ST) candidates 17 2. Particularly Vulnerable Tribal Groups (PVTG) 03 ﻿ Total 20 Subjects and Slots covered under the Scheme: The subjects/disciplines in which student can opt for studies abroad and the number of slots available under each field for grant of award are listed below: - Field of study Number of slots for the field of study Pure/Applied Science/ Engineering/Technology/ Mathematics (STEM) 10 Management, Economics, Finance, Law 04 Agriculture/Medicine 04 Humanities/Social Science/Fine Arts 02 Duration of award with Financial Assistance: Financial assistance will be provided till completion of the course/research or the prescribed duration of the course, whichever is earlier: - Sl. No Course Maximum Duration 1. Post-Doctoral Research 2 years 2. Ph. D 4 years (four years) 3. Master's Degree 1 or 2 years (One/Two years) depending upon the type and duration of the Course.
- **Eligibility:** The applicant must be from a Scheduled Tribe (ST). The applicant must be pursuing a post-graduate course (Master, Ph.D., or Post-Doctoral Research) from a foreign institute/university. The annual income of the family of the applicant (from all sources) should not be greater than ₹ 6,00,000/-. The applicant must have secured at least 55% marks or equivalent grade in the qualifying examination (In the case of Post-Doctoral Research, the qualifying exam is Ph.D.; In the case of Ph.D., the qualifying exam is a Master’s Degree; In the case of a Master’s Degree, the qualifying exam is a Bachelor's Degree) The applicant must be the only child in the family who is availing/has availed of this scholarship. Age Criteria:- If pursuing Post-Doctoral Research, the age of the applicant as on 1st July of the selection year, should not be greater than 38 years. If pursuing Ph.D., the age of the applicant as on 1st July of the selection year, should not be greater than 35 years. If pursuing Masters, the age of the applicant as on 1st July of the selection year, should not be greater than 32 years. Income Criteria:- Scholarships will be paid to the students whose family income from all sources does not exceed ₹ 6,00,000/- (Rupees Six lakhs only) per annum. The family income shall be computed in the following manner: - In case where both father and mother are working, the combined income of both of them from all sources shall be taken into account in computing total family income. In case any other member of the family, other than father and mother, is an earning member, his or her income shall not be included in computing total family income. In case only one parent is alive, the income of that parent shall be taken into account for considering total family income. If other sibling or family member is an earning member, their income shall not be included in computing total family income. In case of an orphan, supported by a guardian, income criteria shall not apply. Note:- 30% of the awards for each year shall be earmarked for women candidates. However, in case, adequate women candidates are not available as per the stipulations of the scheme, then the unutilized slots will be utilized by selecting suitable male candidates. There are 17 slots for ST candidates and 3 slots for PVTG candidates. An individual is eligible for only one award and cannot be considered for any other award or same/higher level of award for the second time under the Scheme. Other Conditions:- Selected candidates shall furnish all such documents and enter into such agreements before their departure as shall be decided by the Government of India from time to time. In case the candidate is already residing abroad, he/she shall furnish all relevant documents and enter into such agreements prior to the release of the scholarship by the Indian Mission. The candidate shall not change the course of study or research and the Institute for which scholarship has been sanctioned. It will be the responsibility of candidate to obtain the appropriate visa for a country wherein he/she intends to study. In case the awardee has received overpayment through Indian Mission abroad or any other Government agency, he/she shall refund the same to Indian Mission abroad. After completion of the course, the awardee shall upload the course completion details along with brief of study in the Alumni Module of National Overseas Scholarship (NOS) portal of the Ministry before his return tickets are booked. Criteria for preparation of Merit List:- All applications received within the stipulated period, will be scrutinized for the eligibility criteria. Separate merit list will be drawn for each field of study. The eligible applications will be considered for award of scholarship as per the procedure given below: First priority will be given to the candidates who have already got admission and are pursuing their studies in the top 1,000 ranked foreign Institutes/Universities (as per the latest QS world ranking). The merit list will be drawn based on the ranking of the Institute. In case of a tie between the QS rankings of two or more candidates, merit will be decided on the basis of marks/grades secured by the candidate in the qualifying examination for higher studies for which the scholarship has been applied for. In case sufficient number of students are not selected as mentioned in para (a) above, merit list will be drawn from the candidates who have already secured preliminary letter/offer of admission from top 1,000 ranked foreign Institutes/Universities (as per the QS world ranking) and are yet to join. Merit list will be drawn in similar manner as mentioned in para ‘a’ above; i.e. based on the ranking of the Institute and in case of tie in ranking of university/institution, the marks/grades secured by the candidate in the qualifying examination. In case sufficient students are not selected as per para “1” and “2” above, the vacant slots will be filled from among the remaining eligible candidates through personal interview by a committee of experts constituted by the Ministry. The candidates who have cleared GRE/GMAT/TOFEL etc. will be given preference.
- **Benefits/scope:** ﻿ Sl. No. Scholarship Component Details 1. Annual Maintenance Allowance The Annual maintenance allowance in USD15,400 ($ Fifteen thousand four hundred only) in US/ Pound sterling 9,900 (£ Nine thousand nine hundred only) in United Kingdom for all level courses. For other countries, the USD or equivalent rates would be applicable. 2. Annual Contingency and Equipment Allowance The Annual Contingency and Equipment Allowance for books/essential apparatus/study tour/typing and binding of thesis etc. will be $ 1532 (US Dollars One thousand five hundred thirty-two only) for the candidates in US and for candidates in United Kingdom, it will be £ 1116 (Pounds sterling One thousand one hundred sixteen only). For other countries, US Dollar or equivalent rates would be applicable. 3. Poll Tax Actuals shall be paid, wherever applicable. 4. Visa Fees Actual visa fees in Indian Rupees will be paid. 5. Incidental Journey Expenses Incidental journey expenses up to US Dollars 20 or its equivalent in Indian Rupees are permissible. 6. Fees Tuition fees and other non-refundable fees which is required to be compulsorily paid by the student for completion of the course, as per actuals. 7. Medical Insurance Premium Actuals as charged will be admissible. The Indian Embassy/Mission in the respective country will however examine the reasonableness of medical premium opted/claimed by the student. 8. Cost of Air Passage Air passage grant on actual basis from India to the nearest place to the educational institution and back to India, by economy class and shortest route at best available price shall be provided. 9. Local Travel Second class railway fare from the port of disembarkation to the place of study and back; in case of far flung places not connected by rail, bus fare from the place of residence to the nearest railway station, actual charge of crossing by ferry, air fare to the nearest rail-cum-air Station will be permissible. Note: Extension of stay beyond prescribed duration for levels of courses as mentioned above, will be without financial assistance of any kind except the air passage to return to India, if the candidate decides to come back to India on completion of the course.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 60

- **Query text:** SC ST scholarship scheme
- **Original source label (unverified):** Central Sector Scheme of Scholarship for College and University Students
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2433
- **Candidate slug:** `csss-cus`
- **Scheme name/title:** Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University students
- **Details:** "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students" is a Scholarship Scheme by the Department of Higher Education, Ministry of Education.  The primary objective of the scheme is to provide financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies. The scholarships are awarded based on the results of the Higher Secondary/ Class 12th Board Examination. A maximum of 82,000 fresh scholarships per annum are provided for pursuing Graduate/ Postgraduate degrees in colleges and universities and for professional courses, such as Medical, Engineering etc.
- **Eligibility:** The applicant must be above the 80th percentile of successful candidates in the relevant stream from the respective Board of Examination in Class 12th of 10+2 pattern or equivalent. The applicant must be pursuing regular degree courses. The applicant must be pursuing courses at colleges/ institutions recognized by the All India Council for Technical Education and the respective Regulatory Bodies concerned. The gross parental/ family income of the applicant should not exceed ₹4,50,000/- per annum. For renewal of scholarship in each year of study, besides getting at least 50% marks in the Annual Examination, maintenance of adequate attendance should be at least 75%. The students are required to have bank accounts opened, especially, in their name.
- **Benefits/scope:** Rate of Scholarship ₹12,000/-per annum at the Graduation level for the first three years of College and University courses. ₹20,000 per annum at the Post-graduation level. ₹20,000/-per annum in the 4th and 5th year to the Students pursuing professional courses, in case, where the duration of the course is five (5) years/Integrated course. Students pursuing technical courses such as B.Tech, B.Engg. will get scholarship up to graduation level only i.e. ₹12,000 p.a. for 1st, 2nd, and 3rd year and ₹20,000 in the 4th year. ﻿ Mode of Disbursal The scholarship will be disbursed directly into the savings bank accounts of the beneficiaries through Direct Benefit Transfer (DBT).
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 500
- **Candidate slug:** `pmsoeds`
- **Scheme name/title:** Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India
- **Details:** The "Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India" aims at providing financial assistance to students from the Backward Classes (BC), Economically Weaker Sections (EWS), and Denotified, Nomadic, and Denotified, Nomadic Tribes (DNTs) to pursue higher education. This scholarship aims to alleviate the financial burden on students belonging to these marginalized communities, enabling them to continue their studies and enhance their skills. The scholarship covers tuition fees, maintenance allowances, and other academic expenses. The financial support is extended to students studying in both government and private institutions.
- **Eligibility:** The applicant should be from Other Backward Classes (OBC) / Economically Backward Classes (EBC) or from Denotified, Nomadic, and Semi-Nomadic Tribes (DNT). The applicant should be studying at the post-matriculation or post-secondary stage of education. The applicant should be permanently settled in the State/UT where they are applying. The applicant should be studying in an institution recognized by the All India Survey on Higher Education (AISHE) or Unified District Information System for Education (UDISE). The applicant's institution should have National Assessment and Accreditation Council (NAAC) or National Board of Accreditation (NBA) accreditation. The applicant should maintain Aadhaar-based attendance in the institution. The applicant must have a valid "Freeship Card" issued by the State/District Authority. Preference/Priority/Reservation/Relaxation: A maximum of 20 slots per annum are reserved for Commercial Pilot License courses, including helicopter and multi-engine training.
- **Benefits/scope:** Components of the Scholarship Maintenance allowance for the complete duration of the course. Reimbursement of compulsory non-refundable fees. Study tour charges (if applicable). Thesis typing/printing charges (for research scholars). Book allowance for students pursuing correspondence courses. Additional allowances for students with disabilities. Financial Support Breakdown Category of Courses Academic Allowance (Yearly in ₹) Tuition Fee (Yearly in ₹) Total (Yearly in ₹) Group 1: Degree and Post Graduate level professional courses 10,000 10,000 20,000 Group 2: Other Professional Courses leading to Degree, Diploma, Certificate 8,000 5,000 13,000 Group 3: Graduate and Post Graduate courses not covered under Group 1 &amp; Group 2 6,000 2,000 8,000 Group 4: All post-matriculation (Post Class X level) non-degree courses 5,000 0 5,000 *Students pursuing C.A./I.C.W.A./C.S./I.C.F.A. shall be treated as day scholars for academic allowance purposes. *Students studying through correspondence/online courses shall not be eligible for academic allowance. *Tuition fees shall be paid to online/correspondence students. *The State Governments may, if they decide, top up the academic allowance from their own resources. *The scholarship amount will be disbursed annually to the bank account of the beneficiary. *The scholarship continues for the duration of the course, subject to satisfactory academic progress.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2174
- **Candidate slug:** `css-nos-st`
- **Scheme name/title:** National Overseas Scholarship For Scheduled Tribes (ST) Students
- **Details:** A scholarship scheme by the Ministry of Tribal Affairs for regular, full-time students from Scheduled Tribes, to obtain higher education (post-graduate courses viz. Masters, Ph.D. and Post-Doctoral Research) from foreign institutes/universities. The Scheme is implemented through the Indian Embassies/Missions abroad, Ministry of External Affairs. 30% of the scholarship awards are earmarked for female candidates. Bachelor-level courses in any discipline are not covered under the scheme. Financial assistance is provided till completion of the course/research or the prescribed duration of the course, whichever is earlier. Selection is based on Interview based merit list prepared by An Expert Committee. The Scholarship comprises of tuition fee, Annual Maintenance allowance of USD 15400, Contingency Charges of USD 1532, Poll Tax, Visa Fee, Medical Insurance, Cost of Air journey, Incidental Journey expenses. The fields of study covered in this scheme are -: Pure/Applied Science/Engineering/Technology/Mathematics(STEM), Management, Economics, Finance, Law, Agriculture/Medicine, Humanities/Social Science/Fine Arts. Number of Award: 20 awards every year would be sanctioned to ST students as under: Sl. No Category No. of Award 1. Scheduled Tribes (ST) candidates 17 2. Particularly Vulnerable Tribal Groups (PVTG) 03 ﻿ Total 20 Subjects and Slots covered under the Scheme: The subjects/disciplines in which student can opt for studies abroad and the number of slots available under each field for grant of award are listed below: - Field of study Number of slots for the field of study Pure/Applied Science/ Engineering/Technology/ Mathematics (STEM) 10 Management, Economics, Finance, Law 04 Agriculture/Medicine 04 Humanities/Social Science/Fine Arts 02 Duration of award with Financial Assistance: Financial assistance will be provided till completion of the course/research or the prescribed duration of the course, whichever is earlier: - Sl. No Course Maximum Duration 1. Post-Doctoral Research 2 years 2. Ph. D 4 years (four years) 3. Master's Degree 1 or 2 years (One/Two years) depending upon the type and duration of the Course.
- **Eligibility:** The applicant must be from a Scheduled Tribe (ST). The applicant must be pursuing a post-graduate course (Master, Ph.D., or Post-Doctoral Research) from a foreign institute/university. The annual income of the family of the applicant (from all sources) should not be greater than ₹ 6,00,000/-. The applicant must have secured at least 55% marks or equivalent grade in the qualifying examination (In the case of Post-Doctoral Research, the qualifying exam is Ph.D.; In the case of Ph.D., the qualifying exam is a Master’s Degree; In the case of a Master’s Degree, the qualifying exam is a Bachelor's Degree) The applicant must be the only child in the family who is availing/has availed of this scholarship. Age Criteria:- If pursuing Post-Doctoral Research, the age of the applicant as on 1st July of the selection year, should not be greater than 38 years. If pursuing Ph.D., the age of the applicant as on 1st July of the selection year, should not be greater than 35 years. If pursuing Masters, the age of the applicant as on 1st July of the selection year, should not be greater than 32 years. Income Criteria:- Scholarships will be paid to the students whose family income from all sources does not exceed ₹ 6,00,000/- (Rupees Six lakhs only) per annum. The family income shall be computed in the following manner: - In case where both father and mother are working, the combined income of both of them from all sources shall be taken into account in computing total family income. In case any other member of the family, other than father and mother, is an earning member, his or her income shall not be included in computing total family income. In case only one parent is alive, the income of that parent shall be taken into account for considering total family income. If other sibling or family member is an earning member, their income shall not be included in computing total family income. In case of an orphan, supported by a guardian, income criteria shall not apply. Note:- 30% of the awards for each year shall be earmarked for women candidates. However, in case, adequate women candidates are not available as per the stipulations of the scheme, then the unutilized slots will be utilized by selecting suitable male candidates. There are 17 slots for ST candidates and 3 slots for PVTG candidates. An individual is eligible for only one award and cannot be considered for any other award or same/higher level of award for the second time under the Scheme. Other Conditions:- Selected candidates shall furnish all such documents and enter into such agreements before their departure as shall be decided by the Government of India from time to time. In case the candidate is already residing abroad, he/she shall furnish all relevant documents and enter into such agreements prior to the release of the scholarship by the Indian Mission. The candidate shall not change the course of study or research and the Institute for which scholarship has been sanctioned. It will be the responsibility of candidate to obtain the appropriate visa for a country wherein he/she intends to study. In case the awardee has received overpayment through Indian Mission abroad or any other Government agency, he/she shall refund the same to Indian Mission abroad. After completion of the course, the awardee shall upload the course completion details along with brief of study in the Alumni Module of National Overseas Scholarship (NOS) portal of the Ministry before his return tickets are booked. Criteria for preparation of Merit List:- All applications received within the stipulated period, will be scrutinized for the eligibility criteria. Separate merit list will be drawn for each field of study. The eligible applications will be considered for award of scholarship as per the procedure given below: First priority will be given to the candidates who have already got admission and are pursuing their studies in the top 1,000 ranked foreign Institutes/Universities (as per the latest QS world ranking). The merit list will be drawn based on the ranking of the Institute. In case of a tie between the QS rankings of two or more candidates, merit will be decided on the basis of marks/grades secured by the candidate in the qualifying examination for higher studies for which the scholarship has been applied for. In case sufficient number of students are not selected as mentioned in para (a) above, merit list will be drawn from the candidates who have already secured preliminary letter/offer of admission from top 1,000 ranked foreign Institutes/Universities (as per the QS world ranking) and are yet to join. Merit list will be drawn in similar manner as mentioned in para ‘a’ above; i.e. based on the ranking of the Institute and in case of tie in ranking of university/institution, the marks/grades secured by the candidate in the qualifying examination. In case sufficient students are not selected as per para “1” and “2” above, the vacant slots will be filled from among the remaining eligible candidates through personal interview by a committee of experts constituted by the Ministry. The candidates who have cleared GRE/GMAT/TOFEL etc. will be given preference.
- **Benefits/scope:** ﻿ Sl. No. Scholarship Component Details 1. Annual Maintenance Allowance The Annual maintenance allowance in USD15,400 ($ Fifteen thousand four hundred only) in US/ Pound sterling 9,900 (£ Nine thousand nine hundred only) in United Kingdom for all level courses. For other countries, the USD or equivalent rates would be applicable. 2. Annual Contingency and Equipment Allowance The Annual Contingency and Equipment Allowance for books/essential apparatus/study tour/typing and binding of thesis etc. will be $ 1532 (US Dollars One thousand five hundred thirty-two only) for the candidates in US and for candidates in United Kingdom, it will be £ 1116 (Pounds sterling One thousand one hundred sixteen only). For other countries, US Dollar or equivalent rates would be applicable. 3. Poll Tax Actuals shall be paid, wherever applicable. 4. Visa Fees Actual visa fees in Indian Rupees will be paid. 5. Incidental Journey Expenses Incidental journey expenses up to US Dollars 20 or its equivalent in Indian Rupees are permissible. 6. Fees Tuition fees and other non-refundable fees which is required to be compulsorily paid by the student for completion of the course, as per actuals. 7. Medical Insurance Premium Actuals as charged will be admissible. The Indian Embassy/Mission in the respective country will however examine the reasonableness of medical premium opted/claimed by the student. 8. Cost of Air Passage Air passage grant on actual basis from India to the nearest place to the educational institution and back to India, by economy class and shortest route at best available price shall be provided. 9. Local Travel Second class railway fare from the port of disembarkation to the place of study and back; in case of far flung places not connected by rail, bus fare from the place of residence to the nearest railway station, actual charge of crossing by ferry, air fare to the nearest rail-cum-air Station will be permissible. Note: Extension of stay beyond prescribed duration for levels of courses as mentioned above, will be without financial assistance of any kind except the air passage to return to India, if the candidate decides to come back to India on completion of the course.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 61

- **Query text:** reserved category student benefits
- **Original source label (unverified):** Central Sector Scheme of Scholarship for College and University Students
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2433
- **Candidate slug:** `csss-cus`
- **Scheme name/title:** Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University students
- **Details:** "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students" is a Scholarship Scheme by the Department of Higher Education, Ministry of Education.  The primary objective of the scheme is to provide financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies. The scholarships are awarded based on the results of the Higher Secondary/ Class 12th Board Examination. A maximum of 82,000 fresh scholarships per annum are provided for pursuing Graduate/ Postgraduate degrees in colleges and universities and for professional courses, such as Medical, Engineering etc.
- **Eligibility:** The applicant must be above the 80th percentile of successful candidates in the relevant stream from the respective Board of Examination in Class 12th of 10+2 pattern or equivalent. The applicant must be pursuing regular degree courses. The applicant must be pursuing courses at colleges/ institutions recognized by the All India Council for Technical Education and the respective Regulatory Bodies concerned. The gross parental/ family income of the applicant should not exceed ₹4,50,000/- per annum. For renewal of scholarship in each year of study, besides getting at least 50% marks in the Annual Examination, maintenance of adequate attendance should be at least 75%. The students are required to have bank accounts opened, especially, in their name.
- **Benefits/scope:** Rate of Scholarship ₹12,000/-per annum at the Graduation level for the first three years of College and University courses. ₹20,000 per annum at the Post-graduation level. ₹20,000/-per annum in the 4th and 5th year to the Students pursuing professional courses, in case, where the duration of the course is five (5) years/Integrated course. Students pursuing technical courses such as B.Tech, B.Engg. will get scholarship up to graduation level only i.e. ₹12,000 p.a. for 1st, 2nd, and 3rd year and ₹20,000 in the 4th year. ﻿ Mode of Disbursal The scholarship will be disbursed directly into the savings bank accounts of the beneficiaries through Direct Benefit Transfer (DBT).
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 500
- **Candidate slug:** `pmsoeds`
- **Scheme name/title:** Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India
- **Details:** The "Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India" aims at providing financial assistance to students from the Backward Classes (BC), Economically Weaker Sections (EWS), and Denotified, Nomadic, and Denotified, Nomadic Tribes (DNTs) to pursue higher education. This scholarship aims to alleviate the financial burden on students belonging to these marginalized communities, enabling them to continue their studies and enhance their skills. The scholarship covers tuition fees, maintenance allowances, and other academic expenses. The financial support is extended to students studying in both government and private institutions.
- **Eligibility:** The applicant should be from Other Backward Classes (OBC) / Economically Backward Classes (EBC) or from Denotified, Nomadic, and Semi-Nomadic Tribes (DNT). The applicant should be studying at the post-matriculation or post-secondary stage of education. The applicant should be permanently settled in the State/UT where they are applying. The applicant should be studying in an institution recognized by the All India Survey on Higher Education (AISHE) or Unified District Information System for Education (UDISE). The applicant's institution should have National Assessment and Accreditation Council (NAAC) or National Board of Accreditation (NBA) accreditation. The applicant should maintain Aadhaar-based attendance in the institution. The applicant must have a valid "Freeship Card" issued by the State/District Authority. Preference/Priority/Reservation/Relaxation: A maximum of 20 slots per annum are reserved for Commercial Pilot License courses, including helicopter and multi-engine training.
- **Benefits/scope:** Components of the Scholarship Maintenance allowance for the complete duration of the course. Reimbursement of compulsory non-refundable fees. Study tour charges (if applicable). Thesis typing/printing charges (for research scholars). Book allowance for students pursuing correspondence courses. Additional allowances for students with disabilities. Financial Support Breakdown Category of Courses Academic Allowance (Yearly in ₹) Tuition Fee (Yearly in ₹) Total (Yearly in ₹) Group 1: Degree and Post Graduate level professional courses 10,000 10,000 20,000 Group 2: Other Professional Courses leading to Degree, Diploma, Certificate 8,000 5,000 13,000 Group 3: Graduate and Post Graduate courses not covered under Group 1 &amp; Group 2 6,000 2,000 8,000 Group 4: All post-matriculation (Post Class X level) non-degree courses 5,000 0 5,000 *Students pursuing C.A./I.C.W.A./C.S./I.C.F.A. shall be treated as day scholars for academic allowance purposes. *Students studying through correspondence/online courses shall not be eligible for academic allowance. *Tuition fees shall be paid to online/correspondence students. *The State Governments may, if they decide, top up the academic allowance from their own resources. *The scholarship amount will be disbursed annually to the bank account of the beneficiary. *The scholarship continues for the duration of the course, subject to satisfactory academic progress.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2174
- **Candidate slug:** `css-nos-st`
- **Scheme name/title:** National Overseas Scholarship For Scheduled Tribes (ST) Students
- **Details:** A scholarship scheme by the Ministry of Tribal Affairs for regular, full-time students from Scheduled Tribes, to obtain higher education (post-graduate courses viz. Masters, Ph.D. and Post-Doctoral Research) from foreign institutes/universities. The Scheme is implemented through the Indian Embassies/Missions abroad, Ministry of External Affairs. 30% of the scholarship awards are earmarked for female candidates. Bachelor-level courses in any discipline are not covered under the scheme. Financial assistance is provided till completion of the course/research or the prescribed duration of the course, whichever is earlier. Selection is based on Interview based merit list prepared by An Expert Committee. The Scholarship comprises of tuition fee, Annual Maintenance allowance of USD 15400, Contingency Charges of USD 1532, Poll Tax, Visa Fee, Medical Insurance, Cost of Air journey, Incidental Journey expenses. The fields of study covered in this scheme are -: Pure/Applied Science/Engineering/Technology/Mathematics(STEM), Management, Economics, Finance, Law, Agriculture/Medicine, Humanities/Social Science/Fine Arts. Number of Award: 20 awards every year would be sanctioned to ST students as under: Sl. No Category No. of Award 1. Scheduled Tribes (ST) candidates 17 2. Particularly Vulnerable Tribal Groups (PVTG) 03 ﻿ Total 20 Subjects and Slots covered under the Scheme: The subjects/disciplines in which student can opt for studies abroad and the number of slots available under each field for grant of award are listed below: - Field of study Number of slots for the field of study Pure/Applied Science/ Engineering/Technology/ Mathematics (STEM) 10 Management, Economics, Finance, Law 04 Agriculture/Medicine 04 Humanities/Social Science/Fine Arts 02 Duration of award with Financial Assistance: Financial assistance will be provided till completion of the course/research or the prescribed duration of the course, whichever is earlier: - Sl. No Course Maximum Duration 1. Post-Doctoral Research 2 years 2. Ph. D 4 years (four years) 3. Master's Degree 1 or 2 years (One/Two years) depending upon the type and duration of the Course.
- **Eligibility:** The applicant must be from a Scheduled Tribe (ST). The applicant must be pursuing a post-graduate course (Master, Ph.D., or Post-Doctoral Research) from a foreign institute/university. The annual income of the family of the applicant (from all sources) should not be greater than ₹ 6,00,000/-. The applicant must have secured at least 55% marks or equivalent grade in the qualifying examination (In the case of Post-Doctoral Research, the qualifying exam is Ph.D.; In the case of Ph.D., the qualifying exam is a Master’s Degree; In the case of a Master’s Degree, the qualifying exam is a Bachelor's Degree) The applicant must be the only child in the family who is availing/has availed of this scholarship. Age Criteria:- If pursuing Post-Doctoral Research, the age of the applicant as on 1st July of the selection year, should not be greater than 38 years. If pursuing Ph.D., the age of the applicant as on 1st July of the selection year, should not be greater than 35 years. If pursuing Masters, the age of the applicant as on 1st July of the selection year, should not be greater than 32 years. Income Criteria:- Scholarships will be paid to the students whose family income from all sources does not exceed ₹ 6,00,000/- (Rupees Six lakhs only) per annum. The family income shall be computed in the following manner: - In case where both father and mother are working, the combined income of both of them from all sources shall be taken into account in computing total family income. In case any other member of the family, other than father and mother, is an earning member, his or her income shall not be included in computing total family income. In case only one parent is alive, the income of that parent shall be taken into account for considering total family income. If other sibling or family member is an earning member, their income shall not be included in computing total family income. In case of an orphan, supported by a guardian, income criteria shall not apply. Note:- 30% of the awards for each year shall be earmarked for women candidates. However, in case, adequate women candidates are not available as per the stipulations of the scheme, then the unutilized slots will be utilized by selecting suitable male candidates. There are 17 slots for ST candidates and 3 slots for PVTG candidates. An individual is eligible for only one award and cannot be considered for any other award or same/higher level of award for the second time under the Scheme. Other Conditions:- Selected candidates shall furnish all such documents and enter into such agreements before their departure as shall be decided by the Government of India from time to time. In case the candidate is already residing abroad, he/she shall furnish all relevant documents and enter into such agreements prior to the release of the scholarship by the Indian Mission. The candidate shall not change the course of study or research and the Institute for which scholarship has been sanctioned. It will be the responsibility of candidate to obtain the appropriate visa for a country wherein he/she intends to study. In case the awardee has received overpayment through Indian Mission abroad or any other Government agency, he/she shall refund the same to Indian Mission abroad. After completion of the course, the awardee shall upload the course completion details along with brief of study in the Alumni Module of National Overseas Scholarship (NOS) portal of the Ministry before his return tickets are booked. Criteria for preparation of Merit List:- All applications received within the stipulated period, will be scrutinized for the eligibility criteria. Separate merit list will be drawn for each field of study. The eligible applications will be considered for award of scholarship as per the procedure given below: First priority will be given to the candidates who have already got admission and are pursuing their studies in the top 1,000 ranked foreign Institutes/Universities (as per the latest QS world ranking). The merit list will be drawn based on the ranking of the Institute. In case of a tie between the QS rankings of two or more candidates, merit will be decided on the basis of marks/grades secured by the candidate in the qualifying examination for higher studies for which the scholarship has been applied for. In case sufficient number of students are not selected as mentioned in para (a) above, merit list will be drawn from the candidates who have already secured preliminary letter/offer of admission from top 1,000 ranked foreign Institutes/Universities (as per the QS world ranking) and are yet to join. Merit list will be drawn in similar manner as mentioned in para ‘a’ above; i.e. based on the ranking of the Institute and in case of tie in ranking of university/institution, the marks/grades secured by the candidate in the qualifying examination. In case sufficient students are not selected as per para “1” and “2” above, the vacant slots will be filled from among the remaining eligible candidates through personal interview by a committee of experts constituted by the Ministry. The candidates who have cleared GRE/GMAT/TOFEL etc. will be given preference.
- **Benefits/scope:** ﻿ Sl. No. Scholarship Component Details 1. Annual Maintenance Allowance The Annual maintenance allowance in USD15,400 ($ Fifteen thousand four hundred only) in US/ Pound sterling 9,900 (£ Nine thousand nine hundred only) in United Kingdom for all level courses. For other countries, the USD or equivalent rates would be applicable. 2. Annual Contingency and Equipment Allowance The Annual Contingency and Equipment Allowance for books/essential apparatus/study tour/typing and binding of thesis etc. will be $ 1532 (US Dollars One thousand five hundred thirty-two only) for the candidates in US and for candidates in United Kingdom, it will be £ 1116 (Pounds sterling One thousand one hundred sixteen only). For other countries, US Dollar or equivalent rates would be applicable. 3. Poll Tax Actuals shall be paid, wherever applicable. 4. Visa Fees Actual visa fees in Indian Rupees will be paid. 5. Incidental Journey Expenses Incidental journey expenses up to US Dollars 20 or its equivalent in Indian Rupees are permissible. 6. Fees Tuition fees and other non-refundable fees which is required to be compulsorily paid by the student for completion of the course, as per actuals. 7. Medical Insurance Premium Actuals as charged will be admissible. The Indian Embassy/Mission in the respective country will however examine the reasonableness of medical premium opted/claimed by the student. 8. Cost of Air Passage Air passage grant on actual basis from India to the nearest place to the educational institution and back to India, by economy class and shortest route at best available price shall be provided. 9. Local Travel Second class railway fare from the port of disembarkation to the place of study and back; in case of far flung places not connected by rail, bus fare from the place of residence to the nearest railway station, actual charge of crossing by ferry, air fare to the nearest rail-cum-air Station will be permissible. Note: Extension of stay beyond prescribed duration for levels of courses as mentioned above, will be without financial assistance of any kind except the air passage to return to India, if the candidate decides to come back to India on completion of the course.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 62

- **Query text:** caste based assistance education
- **Original source label (unverified):** Central Sector Scheme of Scholarship for College and University Students
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 2433
- **Candidate slug:** `csss-cus`
- **Scheme name/title:** Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University students
- **Details:** "Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) Central Sector Scheme of Scholarship for College and University Students" is a Scholarship Scheme by the Department of Higher Education, Ministry of Education.  The primary objective of the scheme is to provide financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies. The scholarships are awarded based on the results of the Higher Secondary/ Class 12th Board Examination. A maximum of 82,000 fresh scholarships per annum are provided for pursuing Graduate/ Postgraduate degrees in colleges and universities and for professional courses, such as Medical, Engineering etc.
- **Eligibility:** The applicant must be above the 80th percentile of successful candidates in the relevant stream from the respective Board of Examination in Class 12th of 10+2 pattern or equivalent. The applicant must be pursuing regular degree courses. The applicant must be pursuing courses at colleges/ institutions recognized by the All India Council for Technical Education and the respective Regulatory Bodies concerned. The gross parental/ family income of the applicant should not exceed ₹4,50,000/- per annum. For renewal of scholarship in each year of study, besides getting at least 50% marks in the Annual Examination, maintenance of adequate attendance should be at least 75%. The students are required to have bank accounts opened, especially, in their name.
- **Benefits/scope:** Rate of Scholarship ₹12,000/-per annum at the Graduation level for the first three years of College and University courses. ₹20,000 per annum at the Post-graduation level. ₹20,000/-per annum in the 4th and 5th year to the Students pursuing professional courses, in case, where the duration of the course is five (5) years/Integrated course. Students pursuing technical courses such as B.Tech, B.Engg. will get scholarship up to graduation level only i.e. ₹12,000 p.a. for 1st, 2nd, and 3rd year and ₹20,000 in the 4th year. ﻿ Mode of Disbursal The scholarship will be disbursed directly into the savings bank accounts of the beneficiaries through Direct Benefit Transfer (DBT).
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 500
- **Candidate slug:** `pmsoeds`
- **Scheme name/title:** Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India
- **Details:** The "Centrally Sponsored Scheme of Post-Matric Scholarship for OBC, EBC  and DNT Students for studying in India" aims at providing financial assistance to students from the Backward Classes (BC), Economically Weaker Sections (EWS), and Denotified, Nomadic, and Denotified, Nomadic Tribes (DNTs) to pursue higher education. This scholarship aims to alleviate the financial burden on students belonging to these marginalized communities, enabling them to continue their studies and enhance their skills. The scholarship covers tuition fees, maintenance allowances, and other academic expenses. The financial support is extended to students studying in both government and private institutions.
- **Eligibility:** The applicant should be from Other Backward Classes (OBC) / Economically Backward Classes (EBC) or from Denotified, Nomadic, and Semi-Nomadic Tribes (DNT). The applicant should be studying at the post-matriculation or post-secondary stage of education. The applicant should be permanently settled in the State/UT where they are applying. The applicant should be studying in an institution recognized by the All India Survey on Higher Education (AISHE) or Unified District Information System for Education (UDISE). The applicant's institution should have National Assessment and Accreditation Council (NAAC) or National Board of Accreditation (NBA) accreditation. The applicant should maintain Aadhaar-based attendance in the institution. The applicant must have a valid "Freeship Card" issued by the State/District Authority. Preference/Priority/Reservation/Relaxation: A maximum of 20 slots per annum are reserved for Commercial Pilot License courses, including helicopter and multi-engine training.
- **Benefits/scope:** Components of the Scholarship Maintenance allowance for the complete duration of the course. Reimbursement of compulsory non-refundable fees. Study tour charges (if applicable). Thesis typing/printing charges (for research scholars). Book allowance for students pursuing correspondence courses. Additional allowances for students with disabilities. Financial Support Breakdown Category of Courses Academic Allowance (Yearly in ₹) Tuition Fee (Yearly in ₹) Total (Yearly in ₹) Group 1: Degree and Post Graduate level professional courses 10,000 10,000 20,000 Group 2: Other Professional Courses leading to Degree, Diploma, Certificate 8,000 5,000 13,000 Group 3: Graduate and Post Graduate courses not covered under Group 1 &amp; Group 2 6,000 2,000 8,000 Group 4: All post-matriculation (Post Class X level) non-degree courses 5,000 0 5,000 *Students pursuing C.A./I.C.W.A./C.S./I.C.F.A. shall be treated as day scholars for academic allowance purposes. *Students studying through correspondence/online courses shall not be eligible for academic allowance. *Tuition fees shall be paid to online/correspondence students. *The State Governments may, if they decide, top up the academic allowance from their own resources. *The scholarship amount will be disbursed annually to the bank account of the beneficiary. *The scholarship continues for the duration of the course, subject to satisfactory academic progress.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2174
- **Candidate slug:** `css-nos-st`
- **Scheme name/title:** National Overseas Scholarship For Scheduled Tribes (ST) Students
- **Details:** A scholarship scheme by the Ministry of Tribal Affairs for regular, full-time students from Scheduled Tribes, to obtain higher education (post-graduate courses viz. Masters, Ph.D. and Post-Doctoral Research) from foreign institutes/universities. The Scheme is implemented through the Indian Embassies/Missions abroad, Ministry of External Affairs. 30% of the scholarship awards are earmarked for female candidates. Bachelor-level courses in any discipline are not covered under the scheme. Financial assistance is provided till completion of the course/research or the prescribed duration of the course, whichever is earlier. Selection is based on Interview based merit list prepared by An Expert Committee. The Scholarship comprises of tuition fee, Annual Maintenance allowance of USD 15400, Contingency Charges of USD 1532, Poll Tax, Visa Fee, Medical Insurance, Cost of Air journey, Incidental Journey expenses. The fields of study covered in this scheme are -: Pure/Applied Science/Engineering/Technology/Mathematics(STEM), Management, Economics, Finance, Law, Agriculture/Medicine, Humanities/Social Science/Fine Arts. Number of Award: 20 awards every year would be sanctioned to ST students as under: Sl. No Category No. of Award 1. Scheduled Tribes (ST) candidates 17 2. Particularly Vulnerable Tribal Groups (PVTG) 03 ﻿ Total 20 Subjects and Slots covered under the Scheme: The subjects/disciplines in which student can opt for studies abroad and the number of slots available under each field for grant of award are listed below: - Field of study Number of slots for the field of study Pure/Applied Science/ Engineering/Technology/ Mathematics (STEM) 10 Management, Economics, Finance, Law 04 Agriculture/Medicine 04 Humanities/Social Science/Fine Arts 02 Duration of award with Financial Assistance: Financial assistance will be provided till completion of the course/research or the prescribed duration of the course, whichever is earlier: - Sl. No Course Maximum Duration 1. Post-Doctoral Research 2 years 2. Ph. D 4 years (four years) 3. Master's Degree 1 or 2 years (One/Two years) depending upon the type and duration of the Course.
- **Eligibility:** The applicant must be from a Scheduled Tribe (ST). The applicant must be pursuing a post-graduate course (Master, Ph.D., or Post-Doctoral Research) from a foreign institute/university. The annual income of the family of the applicant (from all sources) should not be greater than ₹ 6,00,000/-. The applicant must have secured at least 55% marks or equivalent grade in the qualifying examination (In the case of Post-Doctoral Research, the qualifying exam is Ph.D.; In the case of Ph.D., the qualifying exam is a Master’s Degree; In the case of a Master’s Degree, the qualifying exam is a Bachelor's Degree) The applicant must be the only child in the family who is availing/has availed of this scholarship. Age Criteria:- If pursuing Post-Doctoral Research, the age of the applicant as on 1st July of the selection year, should not be greater than 38 years. If pursuing Ph.D., the age of the applicant as on 1st July of the selection year, should not be greater than 35 years. If pursuing Masters, the age of the applicant as on 1st July of the selection year, should not be greater than 32 years. Income Criteria:- Scholarships will be paid to the students whose family income from all sources does not exceed ₹ 6,00,000/- (Rupees Six lakhs only) per annum. The family income shall be computed in the following manner: - In case where both father and mother are working, the combined income of both of them from all sources shall be taken into account in computing total family income. In case any other member of the family, other than father and mother, is an earning member, his or her income shall not be included in computing total family income. In case only one parent is alive, the income of that parent shall be taken into account for considering total family income. If other sibling or family member is an earning member, their income shall not be included in computing total family income. In case of an orphan, supported by a guardian, income criteria shall not apply. Note:- 30% of the awards for each year shall be earmarked for women candidates. However, in case, adequate women candidates are not available as per the stipulations of the scheme, then the unutilized slots will be utilized by selecting suitable male candidates. There are 17 slots for ST candidates and 3 slots for PVTG candidates. An individual is eligible for only one award and cannot be considered for any other award or same/higher level of award for the second time under the Scheme. Other Conditions:- Selected candidates shall furnish all such documents and enter into such agreements before their departure as shall be decided by the Government of India from time to time. In case the candidate is already residing abroad, he/she shall furnish all relevant documents and enter into such agreements prior to the release of the scholarship by the Indian Mission. The candidate shall not change the course of study or research and the Institute for which scholarship has been sanctioned. It will be the responsibility of candidate to obtain the appropriate visa for a country wherein he/she intends to study. In case the awardee has received overpayment through Indian Mission abroad or any other Government agency, he/she shall refund the same to Indian Mission abroad. After completion of the course, the awardee shall upload the course completion details along with brief of study in the Alumni Module of National Overseas Scholarship (NOS) portal of the Ministry before his return tickets are booked. Criteria for preparation of Merit List:- All applications received within the stipulated period, will be scrutinized for the eligibility criteria. Separate merit list will be drawn for each field of study. The eligible applications will be considered for award of scholarship as per the procedure given below: First priority will be given to the candidates who have already got admission and are pursuing their studies in the top 1,000 ranked foreign Institutes/Universities (as per the latest QS world ranking). The merit list will be drawn based on the ranking of the Institute. In case of a tie between the QS rankings of two or more candidates, merit will be decided on the basis of marks/grades secured by the candidate in the qualifying examination for higher studies for which the scholarship has been applied for. In case sufficient number of students are not selected as mentioned in para (a) above, merit list will be drawn from the candidates who have already secured preliminary letter/offer of admission from top 1,000 ranked foreign Institutes/Universities (as per the QS world ranking) and are yet to join. Merit list will be drawn in similar manner as mentioned in para ‘a’ above; i.e. based on the ranking of the Institute and in case of tie in ranking of university/institution, the marks/grades secured by the candidate in the qualifying examination. In case sufficient students are not selected as per para “1” and “2” above, the vacant slots will be filled from among the remaining eligible candidates through personal interview by a committee of experts constituted by the Ministry. The candidates who have cleared GRE/GMAT/TOFEL etc. will be given preference.
- **Benefits/scope:** ﻿ Sl. No. Scholarship Component Details 1. Annual Maintenance Allowance The Annual maintenance allowance in USD15,400 ($ Fifteen thousand four hundred only) in US/ Pound sterling 9,900 (£ Nine thousand nine hundred only) in United Kingdom for all level courses. For other countries, the USD or equivalent rates would be applicable. 2. Annual Contingency and Equipment Allowance The Annual Contingency and Equipment Allowance for books/essential apparatus/study tour/typing and binding of thesis etc. will be $ 1532 (US Dollars One thousand five hundred thirty-two only) for the candidates in US and for candidates in United Kingdom, it will be £ 1116 (Pounds sterling One thousand one hundred sixteen only). For other countries, US Dollar or equivalent rates would be applicable. 3. Poll Tax Actuals shall be paid, wherever applicable. 4. Visa Fees Actual visa fees in Indian Rupees will be paid. 5. Incidental Journey Expenses Incidental journey expenses up to US Dollars 20 or its equivalent in Indian Rupees are permissible. 6. Fees Tuition fees and other non-refundable fees which is required to be compulsorily paid by the student for completion of the course, as per actuals. 7. Medical Insurance Premium Actuals as charged will be admissible. The Indian Embassy/Mission in the respective country will however examine the reasonableness of medical premium opted/claimed by the student. 8. Cost of Air Passage Air passage grant on actual basis from India to the nearest place to the educational institution and back to India, by economy class and shortest route at best available price shall be provided. 9. Local Travel Second class railway fare from the port of disembarkation to the place of study and back; in case of far flung places not connected by rail, bus fare from the place of residence to the nearest railway station, actual charge of crossing by ferry, air fare to the nearest rail-cum-air Station will be permissible. Note: Extension of stay beyond prescribed duration for levels of courses as mentioned above, will be without financial assistance of any kind except the air passage to return to India, if the candidate decides to come back to India on completion of the course.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 63

- **Query text:** apprenticeship training schemes
- **Original source label (unverified):** Pradhan Mantri Kaushal Vikas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1650
- **Candidate slug:** `kvy`
- **Scheme name/title:** Kaushal Vikas Yojana
- **Details:** This scheme aims to address the skill gap faced by construction workers registered with the Board by providing them with access to essential training opportunities for competency development and technical advancement. Currently, construction workers rely solely on on-the-job experience, lacking formal technical training due to institutional limitations. This hinders their ability to secure fair wages and access better services. Recognizing the financial constraints often preventing workers and their families from pursuing formal training, this scheme offers reimbursement for both training costs and lost wages. By bridging this financial gap, the initiative empowers individuals to elevate their skillsets and career prospects.
- **Eligibility:** Applicant himself or his/her husband/wife/father must be a registered construction worker and his/her contribution must be updated. If the registered worker himself wants to undergo training, then his/her age should be between 18-35. Age dependencies: Dependent wife/ unmarried daughter has no age limit. The maximum age of dependent son is 21 years
- **Benefits/scope:** Training fees and materials: Board will reimburse expenses of institute-fixed fees, textbooks, and other training-related stationery. Exam: After training, will have to pass an assessment test. Wages : In case the registered worker himself receives training, an amount equivalent to the minimum wage of the unskilled worker will be reimbursed but only registered workers are eligible, not dependents.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2432
- **Candidate slug:** `pmsby`
- **Scheme name/title:** Pradhan Mantri Suraksha Bima Yojana
- **Details:** An Accident Insurance Scheme offering accidental death and disability cover for death or disability on account of an accident. Premium: Rs.20/- per annum per member. The premium will be deducted from the account holder’s bank / Post office account through ‘auto debit’ facility on or before 1st June of each annual coverage period under the scheme. Coverage Duration: Coverage under PMJJBY is valid for one year from 1st June to 31st May on payment of annual premium. Accident cover assurance termination: The accident cover of the member shall terminate / be restricted accordingly on any of the following events: •	On attaining age 70 years (age nearer birth day). •	Closure of account with the Bank or insufficiency of balance to keep the insurance in force. In case a member is covered under PMSBY through more than one account and premium is received by insurance company inadvertently, insurance cover will be restricted to Rs. 2 lakh.
- **Eligibility:** Individual bank account holders of participating banks aged between 18 years (completed) and 70 years (age nearer birthday) who give their consent to join / enable auto-debit, will be enrolled into the scheme.
- **Benefits/scope:** On Death- the Nominee shall get Rs. 2 Lakhs. Total and irrecoverable loss of both eyes or loss of use of both hands or feet or loss of sight of one eye and loss of use of hand or foot-  Subscriber shall get Rs. 2 Lakhs. Total and irrecoverable loss of sight of one eye or loss of use of one hand or foot –subscriber shall get Rs. 1 Lakh.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

## Query 64

- **Query text:** technical education support
- **Original source label (unverified):** Pradhan Mantri Kaushal Vikas Yojana
- **Review rule:** Do not infer a decision from this source label. Review each candidate using the adjudication protocol.

### Candidate 1

- **Candidate rank:** 1
- **Candidate dataset row index:** 1650
- **Candidate slug:** `kvy`
- **Scheme name/title:** Kaushal Vikas Yojana
- **Details:** This scheme aims to address the skill gap faced by construction workers registered with the Board by providing them with access to essential training opportunities for competency development and technical advancement. Currently, construction workers rely solely on on-the-job experience, lacking formal technical training due to institutional limitations. This hinders their ability to secure fair wages and access better services. Recognizing the financial constraints often preventing workers and their families from pursuing formal training, this scheme offers reimbursement for both training costs and lost wages. By bridging this financial gap, the initiative empowers individuals to elevate their skillsets and career prospects.
- **Eligibility:** Applicant himself or his/her husband/wife/father must be a registered construction worker and his/her contribution must be updated. If the registered worker himself wants to undergo training, then his/her age should be between 18-35. Age dependencies: Dependent wife/ unmarried daughter has no age limit. The maximum age of dependent son is 21 years
- **Benefits/scope:** Training fees and materials: Board will reimburse expenses of institute-fixed fees, textbooks, and other training-related stationery. Exam: After training, will have to pass an assessment test. Wages : In case the registered worker himself receives training, an amount equivalent to the minimum wage of the unskilled worker will be reimbursed but only registered workers are eligible, not dependents.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 2

- **Candidate rank:** 2
- **Candidate dataset row index:** 2432
- **Candidate slug:** `pmsby`
- **Scheme name/title:** Pradhan Mantri Suraksha Bima Yojana
- **Details:** An Accident Insurance Scheme offering accidental death and disability cover for death or disability on account of an accident. Premium: Rs.20/- per annum per member. The premium will be deducted from the account holder’s bank / Post office account through ‘auto debit’ facility on or before 1st June of each annual coverage period under the scheme. Coverage Duration: Coverage under PMJJBY is valid for one year from 1st June to 31st May on payment of annual premium. Accident cover assurance termination: The accident cover of the member shall terminate / be restricted accordingly on any of the following events: •	On attaining age 70 years (age nearer birth day). •	Closure of account with the Bank or insufficiency of balance to keep the insurance in force. In case a member is covered under PMSBY through more than one account and premium is received by insurance company inadvertently, insurance cover will be restricted to Rs. 2 lakh.
- **Eligibility:** Individual bank account holders of participating banks aged between 18 years (completed) and 70 years (age nearer birthday) who give their consent to join / enable auto-debit, will be enrolled into the scheme.
- **Benefits/scope:** On Death- the Nominee shall get Rs. 2 Lakhs. Total and irrecoverable loss of both eyes or loss of use of both hands or feet or loss of sight of one eye and loss of use of hand or foot-  Subscriber shall get Rs. 2 Lakhs. Total and irrecoverable loss of sight of one eye or loss of use of one hand or foot –subscriber shall get Rs. 1 Lakh.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:

### Candidate 3

- **Candidate rank:** 3
- **Candidate dataset row index:** 2435
- **Candidate slug:** `pmuy`
- **Scheme name/title:** Pradhan Mantri Ujjwala Yojana
- **Details:** In May 2016, the Ministry of Petroleum and Natural Gas (MOPNG), introduced the ‘Pradhan Mantri Ujjwala Yojana’ (PMUY) as a flagship scheme with an objective to make clean cooking fuel such as LPG available to the rural and deprived households which were otherwise using traditional cooking fuels such as firewood, coal, cow-dung cakes etc. Usage of traditional cooking fuels had detrimental impacts on the health of rural women as well as on the environment. The scheme was launched on 1st May 2016 in Ballia, Uttar Pradesh by Hon’ble Prime Minister of India, Shri. Narendra Modi ﻿ The target under the scheme was to release 8 Crore LPG Connections to the deprived households by March 2020. On 7th September 2019, Hon’ble Prime Minister of India handed over the 8th Crore LPG connection in Aurangabad, Maharashtra. The release of 8 Crore LPG connections under the scheme has also helped in increasing the LPG coverage from 62% on 1st May 2016 to 99.8% as on 1st April 2021. Under the Union Budget for FY 21-22, provision for release of additional 1 Crore LPG connections under the PMUY scheme has been made. In this phase, special facility has been given to migrant families. ﻿ ﻿
- **Eligibility:** An adult woman belonging to a poor household and not having an LPG connection in her household will be eligible under UJJWALA 2.0. The beneficiaries should belong to any of the following categories: Eligible as per SECC 2011 list Belongs to SC/ST households, be a beneficiary of Pradhan Mantri Awas Yojana (PMAY), Antyodaya Anna Yojana (AAY), Forest dwellers, Most Backward Classes (MBC), Tea and Ex-Tea Garden Tribes, People residing in river islands (Beneficiary will submit supporting document) If she is not falling in the above 2 categories, then she can stake her claim to be a beneficiary under Poor household by submitting 14-point declaration (as per prescribed format) ﻿
- **Benefits/scope:** Rs. 1600 for a connection 14.2kg cylinder or Rs. 1150 for a 5 kg cylinder. Additionally, All PMUY beneficiaries will be provided with first LPG refill and Stove (hot plate) both free of cost along with their deposit free connection. ﻿ Note: Priority would be given to the states which have lower LPG coverage (Compared to the national average) as on 1st Jan 2016.
- **Source or official-reference fields:**
  - No source or official-reference field is present in the dataset.

**Reviewer fields**

- decision:
- verified_dataset_slug:
- rationale:
- evidence_reference:
- reviewer_id:
- confidence:
- second_review_status:
- notes:
